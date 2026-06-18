import asyncio
from ingest.pipeline.etl import ETL
from internals.database import call_neo4j_connection
from utils.config import settings
from utils.logger import VoyverseLogger
from chat.pipeline import ChatPipeline

logger = VoyverseLogger.get("Main")

import asyncio

async def chat_loop(chat_pipeline: ChatPipeline):
    print("Graph Assistant Initialized.")
    print("Use normal text to chat, or use '/c <cypher_query>' to seed custom graph data.")
    print("---------------------------------------------------------------------------")
    
    # This variable preserves our manually fetched graph data across turns
    seeded_graph_context = None

    while True:
        try:
            user_input = input("Enter your query (or type 'exit' to quit): ").strip()
            
            if user_input.lower() == 'exit' or not user_input:
                print("Exiting...")
                break
            
            # --- CONDITION 1: Manual Cypher Query Mode ---
            if user_input.lower().startswith("/c"):
                # Extract the query text cleanly by stripping the prefix
                cypher_query = user_input[2:].strip()
                if not cypher_query:
                    print("Error: No Cypher query provided after /c\n")
                    continue
                
                print(f"Executing manual query: {cypher_query}")
                
                # Execute and format the custom graph paths
                raw_results = chat_pipeline.execute_query(cypher_query)
                seeded_graph_context = chat_pipeline.format_output(raw_results)
                
                print("--- [Seeded Graph Context] ---")
                print(seeded_graph_context)
                print("------------------------------")
                print("Success: Context stored. Please enter your follow-up question now.\n")
                continue  # Jump back to wait for the user's follow-up question
            
            # --- CONDITION 2: Follow-up Question for Seeded Data ---
            if seeded_graph_context is not None:
                print("Processing question using your custom seeded graph context...")
                
                # Send the data directly to the LLM
                response = await chat_pipeline.send_to_llm(seeded_graph_context, user_input)
                print(f"\nResponse from the model: {response}\n")
                
                # Clear the manual context pool so next queries default back to normal pipeline routing
                seeded_graph_context = None
                
            # --- CONDITION 3: Standard Automatic End-to-End Chat Pipeline ---
            else:
                response = await chat_pipeline.chat(user_input)
                print(f"\nResponse from the model: {response}\n")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred in the execution turn: {e}\n")
            

def main() -> None:
    connection = call_neo4j_connection(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )
    chat_pipeline = ChatPipeline(settings.chat_model,connection)

    abs_path = "/home/aymen/Desktop/my_work/voyverse/src/voyverse/data/stix-atlas.json"

    try:
        if settings.ingest:
            pipeline = ETL(abs_path, connection)
            pipeline.run()
            logger.info(f"model {settings.chat_model} read to chat .")
            print("\n"*100)
        asyncio.run(chat_loop(chat_pipeline))
        
            
    except Exception as e:
        logger.error("An error occurred during the ETL process", exc=e)  # pass exc object, not str — preserves traceback
        raise  # re-raise so the process exits with a non-zero code
    finally:
        connection.close()
        logger.info("Neo4j connection closed")

if __name__ == "__main__":
    main()