from ingest.etl import ETL
from internals.database import call_neo4j_connection
from utils.config import settings
from utils.logger import VoyverseLogger

logger = VoyverseLogger.get("Main")

def main() -> None:
    connection = call_neo4j_connection(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )
    abs_path = "/home/aymen/Desktop/my_work/voyverse/src/voyverse/data/stix-atlas.json"

    try:
        pipeline = ETL(abs_path, connection)
        pipeline.run()
    except Exception as e:
        logger.error("An error occurred during the ETL process", exc=e)  # pass exc object, not str — preserves traceback
        raise  # re-raise so the process exits with a non-zero code
    finally:
        connection.close()
        logger.info("Neo4j connection closed")

if __name__ == "__main__":
    main()