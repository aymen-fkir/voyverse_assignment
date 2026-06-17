import os
from pathlib import Path

def find_project_root(start_path: str) -> Path:
    current_path = Path(start_path)
    while True:
        if os.path.exists(current_path.joinpath(".git")) or os.path.exists(current_path.joinpath("pyproject.toml")) :
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # Reached the root directory
            raise FileNotFoundError("No pyproject.toml or .git file found in the directory tree.")
        current_path = Path(parent_path)