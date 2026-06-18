import httpx
from ollama import AsyncClient
from typing import Union,Any
import asyncio
from internals.database import Neo4jConnection
from utils.schemas import LlmQuery
from utils.logger import VoyverseLogger
from utils.helper import load_prompt


logger = VoyverseLogger.get("ChatPipeline")

class ChatPipeline:
    def __init__(self, model: str, connection: Neo4jConnection):
        self.client_limits = httpx.Limits(
            max_connections=20,          # Total maximum allowed connections
            max_keepalive_connections=5, # How many idle connections to keep open in the pool
            keepalive_expiry=20.0          # Time in seconds to keep idle connections alive
        )

        self.client = AsyncClient(
            timeout=None,
            limits=self.client_limits          # Apply the optimized connection pool
        )
        self.model = model
        self.system_prompt_for_cypher = load_prompt("cypher_extracter")
        self.system_prompt_chat = load_prompt("system_chat")
        self.connection = connection

    async def generate_query_from_llm(self,prompt:str)-> Union[LlmQuery,None]:
        response = await self.client.generate(
            model=self.model,
            prompt=prompt,
            system=self.system_prompt_for_cypher,
            format=LlmQuery.model_json_schema(),
            options={"temperature": 0.0},
        )
        try:
            raw_response = response.response
            logger.info("finish generating query")
            
            if not raw_response:
                logger.error("Received empty response from the model.")
                return None

            return LlmQuery.model_validate_json(raw_response)
        
        except Exception as e:
            logger.error("Error parsing model response", exc=e)
            return None
    
    def create_query(self, llm_query: LlmQuery, hop_number: int = 2) -> str:
        """
        Generates a multi-hop Cypher query with explicit Enum value mapping.
        """
        safe_hops = max(1, hop_number)
        
        # Extract the strict string values from the Enums
        node_a_label = llm_query.node_a.value
        node_b_label = llm_query.node_b.value
        relation_type = llm_query.relation.value

        query = f"""
        // 1. Find the anchor relationship matching the LLM intent
        MATCH path = (anchor_a:{node_a_label})-[:{relation_type}]->(anchor_b:{node_b_label})
        
        // 2. Expand outward from both ends of the anchor path up to N hops
        MATCH multi_path = (anchor_a)-[*0..{safe_hops}]-(connected_node)
        WITH path, multi_path
        MATCH secondary_path = (anchor_b)-[*0..{safe_hops}]-(connected_node_b)
        
        // 3. Gather all distinct paths into a single sequence pool
        WITH collect(path) + collect(multi_path) + collect(secondary_path) AS all_paths
        UNWIND all_paths AS p
        
        // 4. Extract individual structural components to flatten the graph layout
        UNWIND nodes(p) AS n
        UNWIND relationships(p) AS rel
        
        // 5. Return distinct triples so your postprocessor maps them cleanly
        RETURN DISTINCT 
            startNode(rel) AS a, 
            rel AS r, 
            endNode(rel) AS b
        """
        return query
    
    def execute_query(self, query: str) -> list[dict[str,Any]]:
        result = self.connection.query(query)
        logger.info("Executed query against Neo4j", total_records=len(result))
        return result
    


    def format_output(self, query_result: list[dict[str, Any]]) -> str:
        if not query_result:
            return "No relevant information found in the graph database."
        
        formatted_lines = []
        
        for idx, record in enumerate(query_result):
            node_a = record.get("a")
            rel = record.get("r")
            node_b = record.get("b")
            
            if node_a and rel and node_b:
                # 1. Extract Node A properties safely using ._properties fallback
                if hasattr(node_a, "items"):
                    a_props = dict(node_a.items())
                elif hasattr(node_a, "_properties"):
                    a_props = dict(node_a._properties)
                else:
                    a_props = dict(node_a)
                    
                a_name = a_props.pop("name", a_props.get("id", "Unknown"))
                a_label = next(iter(node_a.labels), "Node") if hasattr(node_a, "labels") else "Node"
                
                # 2. Extract Node B properties safely
                if hasattr(node_b, "items"):
                    b_props = dict(node_b.items())
                elif hasattr(node_b, "_properties"):
                    b_props = dict(node_b._properties)
                else:
                    b_props = dict(node_b)
                    
                b_name = b_props.pop("name", b_props.get("id", "Unknown"))
                b_label = next(iter(node_b.labels), "Node") if hasattr(node_b, "labels") else "Node"
                
                # 3. Extract Relationship properties safely
                rel_type = rel.type if hasattr(rel, "type") else "CONNECTED_TO"
                if hasattr(rel, "items"):
                    rel_props = dict(rel.items())
                elif hasattr(rel, "_properties"):
                    rel_props = dict(rel._properties)
                else:
                    rel_props = {}

                # 4. Construct the rich text block
                line = (
                    f"### Graph Path {idx + 1}:\n"
                    f"  * Node A: ({a_name}:{a_label}) -> Attributes: {a_props}\n"
                    f"  * Relationship: -[:{rel_type}]-> Attributes: {rel_props}\n"
                    f"  * Node B: ({b_name}:{b_label}) -> Attributes: {b_props}\n"
                )
                formatted_lines.append(line)
            else:
                # Basic fallback if layout doesn't look like an explicit triple
                flat_record = {k: str(v) for k, v in record.items()}
                formatted_lines.append(f"### Record {idx + 1}:\n  {flat_record}\n")

        return "\n".join(formatted_lines)

    async def send_to_llm(self, formatted_output: str, user_input: str) -> str:
        prompt = f"""
        You are a graph database assistant. The user asked: "{user_input}"
        Here are the relevant graph triples retrieved from the database:
        {formatted_output}
        
        Please provide a concise, human-readable summary of the relationships and insights.
        """
        response = await self.client.generate(
            model=self.model,
            prompt=prompt,
            system=self.system_prompt_chat,
            options={"temperature": 0.3},
        )
        return response.response if response.response else "No summary could be generated."
    
    async def chat(self, user_input: str) -> str:
        prompt = f"User input: {user_input}\nGenerate a Cypher query to retrieve relevant information from the graph database."
        llm_query = await self.generate_query_from_llm(prompt)
        if llm_query is None:
            logger.error("Failed to generate a valid query from LLM.")
            return "sorry no relevant information found in the graph database."
        
        query = self.create_query(llm_query)
        data = self.execute_query(query)

        logger.info("Query executed and data retrieved", total_records=data)
        if not data:
            logger.warning("No data returned from the database for the generated query.")
            return "sorry no relevant information found in the graph database."
        formatted_output = self.format_output(data)
        final_response = await self.send_to_llm(formatted_output, user_input)
        return final_response
    
    
    