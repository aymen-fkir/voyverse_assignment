import asyncio
from concurrent.futures import ProcessPoolExecutor
import json 
from internals.database import call_neo4j_connection,Neo4jConnection
from utils.config import settings
from utils.schemas import Node, Relationship
from ..process.process_strategy import CreateTargetLayers, ProcessStrategyFactory,DummieProcessStrategy,TacticsTechniquesProcessStrategy
from utils.logger import VoyverseLogger

logger = VoyverseLogger.get("ETL")

class ETL:
    def __init__(self, path: str,connection: Neo4jConnection):
        self.path = path
        self._map = {
        "x-mitre-tactic": "tactic",
        "attack-pattern": "technique",
        "course-of-action": "mitigation",
        "campaign": "casestudy",
        'subtechnique-of': 'subtechnique_of', 
        'mitigates': 'mitigates', 
        'uses': 'uses'}

        self.connection:Neo4jConnection = connection
        self.executor = ProcessPoolExecutor()
        self.process_factory = ProcessStrategyFactory()

    def extract(self) -> list:
        with open(self.path, "r") as f:
            data = json.load(f)
        return data["objects"]
    
    def create_target_components(self, data: list[Node]) -> tuple[list[Node], list[Relationship]]:
        strategy = self.process_factory.create_strategy(CreateTargetLayers)
        return strategy.run(data)
    
    async def create_components(self,data: list[dict],chunk_size=100) -> tuple[list[Node], list[Relationship]]:
        loop = asyncio.get_running_loop() 
        entities, relations = [], []
        
        try:
            futures_basic_components = [
                loop.run_in_executor(self.executor, self.process_factory.create_strategy(DummieProcessStrategy).run, data[i:i+chunk_size],self._map)
                for i in range(0, len(data), chunk_size)
            ]
            
            logger.info("Processing data in parallel", total_records=len(data), chunk_size=chunk_size, total_chunks=len(futures_basic_components))
            
            futures_advanced_components = [
                loop.run_in_executor(self.executor, self.process_factory.create_strategy(TacticsTechniquesProcessStrategy).run, data)
            ]


            
            results_basic_components = await asyncio.gather(*futures_basic_components)

            result_advanced_components = await asyncio.gather(*futures_advanced_components)
            
            logger.info("Completed parallel processing", total_chunks=len(results_basic_components))
            logger.info("Completed advanced processing", total_advanced_chunks=len(result_advanced_components))

            for entities_chunk, relations_chunk in results_basic_components:
                entities.extend(entities_chunk)
                relations.extend(relations_chunk)
            
            result_advanced_components = result_advanced_components[0]
            logger.info("->Advanced processing results", total_advanced_relations=len(result_advanced_components))
            relations.extend(result_advanced_components)

        finally:
            self.executor.shutdown(wait=False)

        return entities, relations
    

    def group_by_type(self, data: list[dict],key:str) -> dict[str, list[dict]]:
        grouped = {}

        for item in data:
            item_type = item.get(key)
            if item_type in grouped:
                grouped[item_type].append(item)
            else:
                grouped[item_type] = [item]
        return grouped
    
    #to be optimized
    def load(self, entities: list[Node], relations: list[Relationship]) -> None:
        relations_dict = [rel.model_dump() for rel in relations ]
        entities_dict = [ent.model_dump() for ent in entities ]
        
        grouped_entities = self.group_by_type(entities_dict,"type")
        grouped_relations = self.group_by_type(relations_dict,"relationship_type")

        logger.info("Starting loding phase")
        for type, items in grouped_entities.items():
            logger.info("Preparing to load nodes", node_type=type, count=len(items))
            node_cypher_template = f"""
            MERGE (n:{type} {{id: row.id}})
            SET n.created = row.created,
                n.modified = row.modified,
                n.description = row.description
            """
            jobs_node = self.connection.execute_batch(node_cypher_template, items)
            logger.info("Nodes loaded into Neo4j", nodes=jobs_node)

        for relationship_type, items in grouped_relations.items():
            logger.info("Preparing to load relationships", relationship_type=relationship_type, count=len(items))
            relation_cypher_template = f"""
            MATCH (source {{id: row.source_ref}})
            MATCH (target {{id: row.target_ref}})
            MERGE (source)-[r:{relationship_type}]->(target)
            SET r.created = row.created,
                r.modified = row.modified,
                r.description = row.description
            """
            jobs_relation = self.connection.execute_batch(relation_cypher_template, items)
            logger.info("Data loaded into Neo4j", relationships=jobs_relation)
        
    def run(self):
        data = self.extract()
        entities, relations = asyncio.run(self.create_components(data))
        logger.info("Data processing completed, starting load phase", total_entities=len(entities), total_relationships=len(relations))
        
        logger.info("Creating target components (layers and relationships)")
        target_entities, target_relations = self.create_target_components(entities)
        
        logger.info("Extending entities and relations with target components {target_entities} {target_relations}", 
                    total_target_entities=len(target_entities), total_target_relationships=len(target_relations))


        entities.extend(target_entities)
        relations.extend(target_relations)
        self.load(entities, relations)
