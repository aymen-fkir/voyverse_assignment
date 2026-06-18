from pydantic import BaseModel,field_validator



class Node(BaseModel):
    type : str
    id : str
    created : str
    modified : str
    description : str

    @field_validator("type")
    def validate_type(cls, v):
        allowed_types = {"tactic", "technique", "mitigation", "casestudy"}
        if v not in allowed_types:
            raise ValueError(f"Invalid type: {v}. Must be one of {allowed_types}.")
        return v




class Relationship(BaseModel):
    type : str
    id : str
    source_ref : str
    target_ref : str
    relationship_type : str
    created : str
    modified : str
    description : str

    @field_validator("relationship_type")
    def validate_relationship_type(cls, v):
        allowed_types = {'subtechnique_of', 'mitigates', 'uses',"uses_tactic"}
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type: {v}. Must be one of {allowed_types}.")
        return v