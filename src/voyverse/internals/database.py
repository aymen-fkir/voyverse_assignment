from neo4j import GraphDatabase, Driver, ManagedTransaction
from functools import lru_cache
from typing import List, Dict, Any, Optional,LiteralString,cast
from utils.logger import VoyverseLogger

logger = VoyverseLogger.get("Neo4jConnection")
class Neo4jConnection:
    def __init__(self, uri: str, user: str, password: str):
        self.driver: Driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    #vurnable for cipher injection 
    def query(self, query_param: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a single read/write query in an auto-commit transaction."""
        query_param = cast(LiteralString, query_param)  # Type hinting for safer Cypher queries
        with self.driver.session() as session:
            result = session.run(query_param, parameters)
            return [record.data() for record in result]
    
    def test_connection(self):
        try:
            self.driver.verify_connectivity()
        except Exception as e:
            raise Exception(f"Connection to Neo4j failed: {e}")

    # ==========================================
    # 1. BATCH EXECUTION MODULE
    # ==========================================
    def execute_batch(self, cypher_query: str, batch_data: List[Dict[str, Any]]) -> int:
        """
        Executes a uniform Cypher query over a list of parameter dictionaries using 
        UNWIND, processed inside a single atomic transaction.
        
        Returns the number of elements processed.
        """
        # Wrapping optimization: pass the full array to Neo4j in one single wire call
        wrapped_query = cast(LiteralString,f"""
        UNWIND $batch AS row
        {cypher_query}
        """)
        
        def _batch_work(tx: ManagedTransaction):
            result = tx.run(wrapped_query, {"batch": batch_data})
            # Consuming the summary forces execution and lets us track updates if needed
            return result.consume()
        try:
            with self.driver.session() as session:
                session.execute_write(_batch_work)
        
        except Exception as e:
            logger.error("Batch execution failed", exc=e)
            raise        
        logger.info("Batch execution completed", total_records=len(batch_data))
        return len(batch_data)

    # ==========================================
    # 2. ONTOLOGY CRUD METHODS
    # ==========================================
    
    def upsert_entity(self, label: str, entity_id: str, properties: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create or fully update a single entity node based on its unique STIX or internal ID.
        Dynamically handles labels like Tactic, Technique, Mitigation, CaseStudy.
        """
        
        query = f"""
        MERGE (n:{label} {{id: $entity_id}})
        SET n += $properties
        RETURN n
        """
        return self.query(query, {"entity_id": entity_id, "properties": properties})

    def get_entity(self, label: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific entity's properties from the graph."""
        query = f"""
        MATCH (n:{label} {{id: $entity_id}})
        RETURN n
        """
        records = self.query(query, {"entity_id": entity_id})
        return records[0]['n'] if records else None

    def delete_entity(self, label: str, entity_id: str, detach: bool = True) -> bool:
        """
        Delete an entity node. If detach=True, it drops all incoming/outgoing relationships 
        (essential for maintaining graph integrity without leaving dangling edges).
        """
        prefix = "DETACH " if detach else ""
        query = f"""
        MATCH (n:{label} {{id: $entity_id}})
        {prefix}DELETE n
        """
        self.query(query, {"entity_id": entity_id})
        return True

    def create_relationship(self, source_label: str, source_id: str, 
                            target_label: str, target_id: str, 
                            rel_type: str, rel_properties: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Creates a directional, typed edge between two verified nodes."""
        s_label = "".join(c for c in source_label if c.isalnum() or c == '_')
        t_label = "".join(c for c in target_label if c.isalnum() or c == '_')
        r_type = "".join(c for c in rel_type if c.isalnum() or c == '_').upper()
        
        props = rel_properties or {}
        
        query = f"""
        MATCH (source:{s_label} {{id: $source_id}})
        MATCH (target:{t_label} {{id: $target_id}})
        MERGE (source)-[r:{r_type}]->(target)
        SET r += $props
        RETURN r
        """
        return self.query(query, {"source_id": source_id, "target_id": target_id, "props": props})


@lru_cache(maxsize=1)
def call_neo4j_connection(uri: str, user: str, password: str) -> Neo4jConnection:
    connection = Neo4jConnection(uri, user, password)
    connection.test_connection()
    return connection