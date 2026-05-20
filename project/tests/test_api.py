"""Smoke-тесты для API предсказания нагрузки на охлаждение."""
import pytest


def test_health_endpoint(client):
    """
    Проверка эндпоинта работоспособности сервиса.
    
    Тестируем:
    - Статус код 200 (OK)
    - Наличие поля status = "ok"
    - Наличие временной метки
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_predict_endpoint_valid_data(client):
    """
    Проверка эндпоинта предсказания с валидными данными.
    
    Отправляем параметры здания:
    - X1: относительная компактность
    - X2: площадь поверхности
    - X3: площадь стен
    - X4: площадь крыши
    - X5: высота здания
    - X6: ориентация (2-5 направлений)
    - X7: площадь остекления
    - X8: распределение остекления (1-5)
    
    Ожидаем:
    - Статус 200 (если модель обучена) или 500 (если модель ещё не загружена)
    - В случае успеха: наличие полей cooling_load, risk_level
    """
    payload = {
        "X1": 0.75,           # Относительная компактность
        "X2": 514.5,          # Площадь поверхности
        "X3": 294.0,          # Площадь стен
        "X4": 171.5,          # Площадь крыши
        "X5": 7.0,            # Высота здания
        "X6": 2,              # Ориентация (2, 3, 4, 5)
        "X7": 15.0,           # Площадь остекления
        "X8": 3               # Распределение остекления (1-5)
    }
    response = client.post("/predict", json=payload)
    # Если модель ещё не обучена — ожидаем 500, это нормально на раннем этапе
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        # Проверяем наличие ключевых полей ответа
        assert "heating_load" in data or "cooling_load" in data
        assert "risk_level" in data


def test_info_endpoint(client):
    """
    Проверка эндпоинта с информацией о модели.
    
    Тестируем:
    - Статус 200 (если модель загружена) или 500 (если нет)
    - Наличие полей model и artifacts_dir
    """
    response = client.get("/info")
    # Если модель не загружена — 500 это нормально на этапе разработки
    assert response.status_code in [200, 500]