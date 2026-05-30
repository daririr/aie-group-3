import json
import joblib
from ..config import ARTIFACTS_DIR


class ModelRegistry:
    def __init__(self):
        self.manifest_path = ARTIFACTS_DIR / "models" / "best_model_manifest.json"
        self.manifest = self._load_manifest()
        self.models = self._load_models()

    def _load_manifest(self) -> dict:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_path}")
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_models(self) -> dict:
        models = {}
        for target in self.manifest["targets"]:
            filename = f"{self.manifest['model_name']}_{target}.pkl"
            filepath = ARTIFACTS_DIR / "models" / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Model artifact not found: {filepath}")
            models[target] = joblib.load(filepath)
        return models

    def predict(self, target: str, X) -> list:
        return self.models[target].predict(X)
