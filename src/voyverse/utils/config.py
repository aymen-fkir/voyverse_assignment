from pydantic_settings import BaseSettings
from pathlib import Path
from .helper import find_project_root

class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    chunk_size: int = 10
    model_name: str = "gemma3:1b"
    chat_model: str = "gemma3:1b"
    ingest: bool = False
    class Config:
        PATH_ROOT: Path = find_project_root(__file__)
        env_file = PATH_ROOT.joinpath(".env")
        Extra = "ignore"


settings = Settings() #type:ignore