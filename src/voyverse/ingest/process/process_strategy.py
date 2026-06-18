import uuid
from datetime import datetime
from typing import TypeVar
from collections import defaultdict
from utils.schemas import GatheredData, Node, ProcessedLlmOutput, Relationship,LlmOutputList,ProcessedLlmOutputList,ValidLabel,InpuToLlm
from utils.logger import VoyverseLogger
from utils.config import settings
import asyncio
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


class CreateTargetLayers:
    
    @staticmethod
    def create_node() -> list[Node]:
        
        layers = {"ui":"UI Layer",
         "application":"Application Layer",
         "model":"Model Layer",
         "infrastructure":"Infrastructure Layer",
         "data_sources":"Data Sources Layer"}
        
        nodes: list[Node] = []
        for layer in layers:
            time = str(datetime.now())
            node = Node(
                type=layer,
                id=f"node-{layer}-{str(uuid.uuid4())}",
                created=time,
                modified=time,
                description=layers[layer]
            )
            nodes.append(node)

        return nodes
    
    @staticmethod
    def create_relationships(data:ProcessedLlmOutputList,layers: dict[str,str]) -> list[Relationship]:
        relations = []
        for item in data.root:
            if item.label not in layers:
                raise ValueError(f"Invalid label: {item.label}. Must be one of {list(layers.keys())}.")
            for i,src in enumerate(item.source_ref):
                relation = Relationship(
                    type=f"Target-{item.label}",
                    id=f"layer-{item.label}-{str(uuid.uuid4())}",
                    source_ref=src,
                    target_ref=layers[item.label],
                    relationship_type="Target",
                    created=str(datetime.now()),
                    modified=str(datetime.now()),
                    description=item.reason[i]
                )
                relations.append(relation)

        return relations

    @staticmethod
    def preprocess(data:list[Node])->list[Node]:
        result = []
        for obj in data:
            if obj.type == "technique":
                result.append(obj)
        return result
    @staticmethod
    def classify(data:list[Node]) -> GatheredData:
        from ingest.process.llm_classification import LLMClassification
        llm_classifier = LLMClassification(model_name=settings.model_name, chunk_size=settings.chunk_size)
        input_to_llm = [InpuToLlm(description=item.description, id=item.id) for item in data]
        results = asyncio.run(llm_classifier.run(input_to_llm))
        return results
    
    @staticmethod
    def postprocess(data:GatheredData) -> ProcessedLlmOutputList:
        processed_results = []
        grouped = {ValidLabel.UI: {"reasons": [],"source_refs": []}, ValidLabel.APPLICATION: {"reasons": [],"source_refs": []}, ValidLabel.MODEL: {"reasons": [],"source_refs": []}, ValidLabel.INFRASTRUCTURE: {"reasons": [],"source_refs": []}, ValidLabel.DATA_SOURCES: {"reasons": [],"source_refs": []}}
        for i,item in enumerate(data.root):
            if item.label not in grouped:
                raise ValueError(f"Invalid label: {item.label}. Must be one of {list(grouped.keys())}.")
            grouped[item.label]["reasons"].append(item.reason)
            id_ = data.root[i].id
            grouped[item.label]["source_refs"].append(id_)

        
        for label, content in grouped.items():
            logger.info("Processing LLM results for label", label=label, total_reasons=len(content["reasons"]), total_source_refs=content["source_refs"])
            if content["source_refs"]:  # Only add if there are source_refs
                processed_results.append(ProcessedLlmOutput(label=label, 
                                                            reason=content["reasons"], 
                                                            source_ref=content["source_refs"]))
        return ProcessedLlmOutputList(root=processed_results)

    @staticmethod
    def run(data: list[Node]) -> tuple[list[Node], list[Relationship]]:
        tactics = CreateTargetLayers.preprocess(data)
        logger.info("Preprocessed data for LLM classification", total_tactics=len(tactics))
        llm_results = CreateTargetLayers.classify(tactics)
        logger.info("LLM classification completed", total_results=len(llm_results.root))
        processed_results = CreateTargetLayers.postprocess(llm_results)
        logger.info("Postprocessed LLM results", total_processed_results=len(processed_results.root))
        layers_nodes = CreateTargetLayers.create_node()
        layers_dict = {node.type: node.id for node in layers_nodes}
        relationships = CreateTargetLayers.create_relationships(processed_results, layers_dict)
        logger.info("Created relationships between tactics and layers", total_relationships=len(relationships))
        return layers_nodes, relationships
    

T = TypeVar('T')

class ProcessStrategyFactory:
    @staticmethod
    def create_strategy[T](strategy_class: type[T]) -> T:
        if strategy_class is DummieProcessStrategy:
            return DummieProcessStrategy() #type: ignore
        elif strategy_class is TacticsTechniquesProcessStrategy:
            return TacticsTechniquesProcessStrategy() #type: ignore
        elif strategy_class is CreateTargetLayers:
            return CreateTargetLayers() #type: ignore
        else:
            raise ValueError(f"Unknown strategy: {strategy_class}")
        