import json
import joblib
import logging
from pathlib import Path
from .config import MANIFEST_PATH, MODELS_DIR

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Загружает манифест эксперимента и соответствующие сериализованные модели."""

    def __init__(self, manifest_path: Path = MANIFEST_PATH):
        self.manifest = self._load_manifest(manifest_path)
        self.models = self._load_models()

    def _load_manifest(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        logger.info("Loaded manifest for model: %s", manifest["model_name"])
        return manifest

    def _load_models(self) -> dict:
        models = {}
        model_name = self.manifest["model_name"]
        for target in self.manifest["targets"]:
            filename = f"{model_name}_{target}.pkl"
            filepath = MODELS_DIR / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Model artifact not found: {filepath}")
            models[target] = joblib.load(filepath)
            logger.info("Loaded pipeline for %s: %s", target, filepath.name)
        return models

    def get_model(self, target: str):
        return self.models.get(target)

    def get_features(self) -> dict:
        return self.manifest.get("features", {})
