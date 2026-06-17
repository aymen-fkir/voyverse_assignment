from utils.schemas import Node, Relationship

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
    


class ProcessStrategyFactory:
    @staticmethod
    def create_strategy(strategy_name: str) -> DummieProcessStrategy:
        if strategy_name == "dummie":
            return DummieProcessStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")