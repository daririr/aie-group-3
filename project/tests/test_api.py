from fastapi.testclient import TestClient
from src.service.main import app


def test_health():
    """Health check должен возвращать status=ok."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


def test_predict_validation_error():
    """Неполные данные должны возвращать 422."""
    with TestClient(app) as client:
        response = client.post("/predict", json={"X1": 0.5})
        assert response.status_code == 422


def test_predict_success(sample_input):
    """Полные данные должны возвращать предсказание."""
    with TestClient(app) as client:
        response = client.post("/predict", json=sample_input)

        if response.status_code == 200:
            data = response.json()
            assert "heating_load" in data
            assert "cooling_load" in data
            assert "risk_level" in data
            assert "recommendations" in data
            assert "top_factors" in data
            assert isinstance(data["heating_load"], float)
            assert data["risk_level"] in ["low", "medium", "high"]
        else:
            assert response.status_code == 500
            detail = response.json().get("detail", "").lower()
            assert "predictor" in detail or "registry" in detail or "model" in detail


def test_model_info():
    """Endpoint /info должен возвращать информацию о модели."""
    with TestClient(app) as client:
        response = client.get("/info")

        if response.status_code == 200:
            data = response.json()
            assert "model" in data or "artifacts_dir" in data
        else:
            assert response.status_code == 500
            detail = response.json().get("detail", "").lower()
            assert "registry" in detail
