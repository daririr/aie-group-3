import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIGS_DIR = BASE_DIR / "configs"
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", BASE_DIR / "artifacts")).resolve()


def load_yaml(filename: str) -> dict:
    filepath = CONFIGS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
