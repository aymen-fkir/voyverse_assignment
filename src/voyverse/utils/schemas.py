from pydantic import BaseModel,field_validator,Field
from enum import Enum
from typing import Optional
from utils.config import settings


class ValidLabel(str, Enum):
    DATA_SOURCES = "data_sources"
    MODEL = "model"
    APPLICATION = "application"
    INFRASTRUCTURE = "infrastructure"
    UI = "ui"

class ValidRelationshipType(str, Enum):
    SUBTECHNIQUE_OF = "subtechnique_of"
    MITIGATES = "mitigates"
    USES = "uses"
    USES_TACTIC = "uses_tactic"
    TARGET = "Target"


class ValidNodeType(str, Enum):
    TACTIC = "tactic"
    TECHNIQUE = "technique"
    MITIGATION = "mitigation"
    CASESTUDY = "casestudy"
    UI = "ui"
    APPLICATION = "application"
    MODEL = "model"
    INFRASTRUCTURE = "infrastructure"
    DATA_SOURCES = "data_sources"


class Node(BaseModel):
    type : str
    id : str
    created : str
    modified : str
    description : str

    @field_validator("type")
    def validate_type(cls, v):
        allowed_types = {"tactic", "technique", "mitigation", "casestudy","ui","application","model","infrastructure","data_sources"}
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
        allowed_types = {'subtechnique_of', 'mitigates', 'uses',"uses_tactic","Target"}
        if v not in allowed_types:
            raise ValueError(f"Invalid relationship type: {v}. Must be one of {allowed_types}.")
        return v



class LlmOutput(BaseModel):
    label: ValidLabel = Field(description="The label assigned to the input text by the classifier .",
                      examples=["ui","application","model","infrastructure","data_sources"])
    
    reason:str = Field(description="The reason provided by classifier for the assigned label.")
    id : Optional[str] = Field(description="An optional identifier for the input text, useful for tracking and reference purposes.", default=None)



class GatheredData(BaseModel):
    root : list[LlmOutput]

    
class LlmOutputList(BaseModel):
    root: list[LlmOutput] = Field(description="""A list of LlmOutput objects representing 
                                      the classification results for multiple input texts.""",
                                      min_length=settings.chunk_size,
                                      max_length=settings.chunk_size)


class ProcessedLlmOutput(BaseModel):
    label: ValidLabel
    reason:list[str]
    source_ref: list[str] 

class ProcessedLlmOutputList(BaseModel):
    root: list[ProcessedLlmOutput] 


class InpuToLlm(BaseModel):
    description: str
    id: Optional[str] = None


class LlmQuery(BaseModel):
    relation : ValidRelationshipType
    node_a : ValidNodeType
    node_b : ValidNodeType