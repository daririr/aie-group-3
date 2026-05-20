import os
from pathlib import Path

# Базовая директория проекта (папка, в которой лежит src/)
BASE_DIR = Path(__file__).resolve().parents[1]

# Пути к артефактам
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
METRICS_DIR = ARTIFACTS_DIR / "metrics"

MANIFEST_PATH = MODELS_DIR / "best_model_manifest.json"

# Переопределение путей через ENV (для Docker/production)
if os.getenv("ARTIFACTS_DIR"):
    ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR"))
    MODELS_DIR = ARTIFACTS_DIR / "models"
    METRICS_DIR = ARTIFACTS_DIR / "metrics"
    MANIFEST_PATH = MODELS_DIR / "best_model_manifest.json"
