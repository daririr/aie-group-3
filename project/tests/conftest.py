"""Конфигурационный файл для pytest."""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from src.main import app

# Добавляем корень проекта в PYTHONPATH
# Это нужно, чтобы тесты могли импортировать модуль src
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture(scope="function")
def client():
    """
    Фикстура для создания тестового клиента FastAPI.
    
    Эта фикстура:
    1. Корректно инициализирует lifespan (загружает модель)
    2. Создает TestClient для отправки HTTP-запросов
    3. Автоматически закрывает клиент после теста
    """
    with TestClient(app) as test_client:
        yield test_client