import os
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def find_project_root(start_path: str) -> Path:
    current_path = Path(start_path)
    while True:
        if os.path.exists(current_path.joinpath(".git")) or os.path.exists(current_path.joinpath("pyproject.toml")) :
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # Reached the root directory
            raise FileNotFoundError("No pyproject.toml or .git file found in the directory tree.")
        current_path = Path(parent_path)

def load_prompt(prompt_name: str) -> str:
    project_root = find_project_root(__file__)
    prompt_path = project_root /"src" / "voyverse" /"prompts" / f"{prompt_name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file {prompt_path} not found.")
    with open(prompt_path, "r") as file:
        return file.read()