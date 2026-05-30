import pytest
from pathlib import Path
import numpy as np


@pytest.fixture
def artifacts_exist():
    """Проверка наличия артефактов с правильным путём."""
    from pathlib import Path
    from src.config import ARTIFACTS_DIR

    manifest = ARTIFACTS_DIR / "models" / "best_model_manifest.json"

    if not manifest.exists():
        pytest.skip(f"Артефакты не найдены: {manifest}. Запустите эксперимент.")
    return manifest


def test_predictor_import(artifacts_exist):
    """CoolingPredictor должен импортироваться."""
    from src.models.predictor import CoolingPredictor

    assert CoolingPredictor is not None


def test_model_registry_loads(artifacts_exist):
    """ModelRegistry должен загружать модели."""
    from src.models.registry import ModelRegistry

    registry = ModelRegistry()
    assert registry.manifest is not None
    assert "model_name" in registry.manifest
    assert "targets" in registry.manifest
    assert len(registry.models) > 0


def test_risk_levels_logic():
    """Пороги риска должны быть логичными."""
    from src.config import load_yaml

    cfg = load_yaml("serving.yaml")
    thresholds = cfg["risk_thresholds"]
    assert thresholds["low"] < thresholds["medium"]
    assert thresholds["low"] > 0
    assert thresholds["medium"] > 0


def test_predictor_risk_calculation(sample_input):
    """Predictor должен корректно считать риск."""
    from src.models.predictor import CoolingPredictor
    from src.models.registry import ModelRegistry

    registry = ModelRegistry()
    predictor = CoolingPredictor(registry)

    low_risk_input = sample_input.copy()
    low_risk_input["X7"] = 0.0

    result = predictor.predict(low_risk_input)
    assert result["risk_level"] in ["low", "medium"]


def test_recommendations_generation(sample_input):
    """Predictor должен генерировать рекомендации."""
    from src.models.predictor import CoolingPredictor
    from src.models.registry import ModelRegistry

    registry = ModelRegistry()
    predictor = CoolingPredictor(registry)

    result = predictor.predict(sample_input)

    assert isinstance(result["recommendations"], list)
    assert len(result["recommendations"]) > 0
    assert all(isinstance(r, str) for r in result["recommendations"])


def test_preprocessor_build():
    """Preprocessor должен строиться корректно."""
    from src.features.preprocess import build_preprocessor
    from sklearn.compose import ColumnTransformer

    num_cols = ["X1", "X2", "X3"]
    cat_cols = ["X6", "X8"]

    preprocessor = build_preprocessor(num_cols, cat_cols)
    assert isinstance(preprocessor, ColumnTransformer)
    assert len(preprocessor.transformers) == 2
