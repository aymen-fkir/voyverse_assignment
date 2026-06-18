import uuid
from datetime import datetime
from typing import Any,TypeVar
from collections import defaultdict
from utils.schemas import Node, Relationship
from utils.logger import VoyverseLogger

logger = VoyverseLogger.get("ProcessStrategy")

class DummieProcessStrategy:
    """
    Base class for processing strategies.
    Each strategy defines how to transform raw data into a format suitable for database insertion.
    """
    @staticmethod
    def create_node(data:dict,map_:dict) -> Node:

        node_type = map_[data["type"]]
        node = Node(
            type=node_type,
            id=data["id"],
            created=data.get("created", ""),
            modified=data.get("modified", ""),
            description=data.get("description", "")
        )
        return node
    @staticmethod
    def create_relationship(data:dict,map_:dict) -> Relationship:

        relationship = Relationship(
            type="relationship",
            id=data["id"],
            source_ref=data["source_ref"],
            target_ref=data["target_ref"],
            relationship_type=map_[data["relationship_type"]],
            created=data.get("created", ""),
            modified=data.get("modified", ""),
            description=data.get("description", "")
        )
        return relationship
    
    @staticmethod
    def run(data: list[dict], map_:dict) -> tuple[list[Node], list[Relationship]]:
        entities, relations = [], []
        for obj in data:
            if obj.get("type") in map_:
               node = DummieProcessStrategy.create_node(obj, map_)
               entities.append(node)

            elif obj.get("type") == "relationship":
                relationship = DummieProcessStrategy.create_relationship(obj, map_)
                relations.append(relationship)

        return entities, relations
    

class TacticsTechniquesProcessStrategy:
    @staticmethod
    def create_uses_tactic_relationship(key:str,value:str) -> Relationship:

        time = str(datetime.now())
        relation = Relationship(
            type="uses_tactic",
            id="uses-tactic-"+str(uuid.uuid4()),
            source_ref=key,
            target_ref=value,
            relationship_type="uses_tactic",
            created=time,
            modified=time,
            description=f"technique {key} uses tactic {value}"
        )

        return relation
    @staticmethod
    def preprocess(data:list[dict])->tuple[dict[str,str],dict[str,list[str]]]:
        techniques = {}
        tactics = {}
        for obj in data:
            if obj.get("type") == "x-mitre-tactic" :
                tactics[obj["x_mitre_shortname"]] = obj["id"]
            elif obj.get("type") == "attack-pattern" :
                chain = obj.get("kill_chain_phases",[{}])
                for element in chain:
                    phase_name = element.get("phase_name")
                    if phase_name and phase_name in techniques:
                        techniques[obj["id"]].append(phase_name)
                    elif phase_name:
                        techniques[obj["id"]] = [phase_name]

        return tactics,techniques
    
    @staticmethod
    def extract(techniques: dict[str, list[str]], tactics: dict[str, str]) -> dict[str, list[str]]:
        techniques_to_tactics = defaultdict(list)
        for technique, phases_name in techniques.items():
            for phase_name in phases_name:
                if phase_name in tactics:
                    techniques_to_tactics[technique].append(tactics[phase_name])
        return techniques_to_tactics
    
    @staticmethod
    def run(data: list[dict]) -> list[Relationship]:
        tactics, techniques = TacticsTechniquesProcessStrategy.preprocess(data)
        logger.info("Preprocessed data for advanced processing", total_techniques=len(techniques), total_tactics=len(tactics))
        techniques_to_tactics = TacticsTechniquesProcessStrategy.extract(techniques, tactics)
        relationships = []
        for technique, tactics in techniques_to_tactics.items():
            for tactic in tactics:
                relation = TacticsTechniquesProcessStrategy.create_uses_tactic_relationship(technique,tactic)
                relationships.append(relation)

        return relationships


class CreateLayersNode:
    pass

T = TypeVar('T')

class ProcessStrategyFactory:
    @staticmethod
    def create_strategy[T](strategy_class: type[T]) -> T:
        if strategy_class is DummieProcessStrategy:
            return DummieProcessStrategy() #type: ignore
        elif strategy_class is TacticsTechniquesProcessStrategy:
            return TacticsTechniquesProcessStrategy() #type: ignore
        else:
            raise ValueError(f"Unknown strategy: {strategy_class}")
        