# Исходный код проекта

В этой папке находится основной код проекта Energy Efficiency Prediction.

## Структура

src/
├── config.py              # Загрузка YAML-конфигов и пути к файлам
├── service.py             # Точка входа для запуска сервиса
├── train.py               # Точка входа для обучения моделей
│
├── data/                  # Работа с данными
│   ├── __init__.py
│   └── loader.py          # Загрузка и подготовка данных из CSV
│
├── features/              # Инженерия признаков
│   ├── __init__.py
│   └── preprocess.py      # Построение препроцессора (Scaler + Encoder)
│
├── models/                # Модели и предсказания
│   ├── __init__.py
│   ├── registry.py        # Загрузка моделей из артефактов
│   └── predictor.py       # Бизнес-логика предсказаний и рекомендации
│
├── service/               # FastAPI сервис
│   ├── __init__.py
│   ├── main.py            # Основное приложение FastAPI
│   └── schemas.py         # Pydantic схемы для валидации
│
└── utils/                 # Вспомогательные модули
    ├── __init__.py
    └── logging.py         # Настройка логгера (консоль + файл)

## Описание модулей

### config.py
Централизованная загрузка конфигурации и управление путями.

Основные функции:
- load_yaml(filename) — загрузка YAML-конфига из папки configs/
- BASE_DIR — корень проекта
- CONFIGS_DIR, DATA_DIR, ARTIFACTS_DIR — пути к папкам

### data/loader.py
Загрузка и подготовка данных.

Функция load_and_prepare_data():
- Читает CSV с правильными разделителями (; и ,)
- Применяет dropna согласно конфигу
- Разделяет на train/test (80/20)
- Возвращает X_train, X_test, y_train, y_test и списки колонок

### features/preprocess.py
Построение пайплайна предобработки.

Функция build_preprocessor(num_cols, cat_cols):
- StandardScaler для числовых признаков
- OneHotEncoder для категориальных
- Возвращает ColumnTransformer

### models/registry.py
Управление загруженными моделями.

Класс ModelRegistry:
- Загружает манифест из best_model_manifest.json
- Загружает модели (.pkl файлы) для каждого таргета
- Предоставляет метод predict(target, X)

### models/predictor.py
Бизнес-логика предсказаний.

Класс CoolingPredictor:
- Принимает входные данные (словарь)
- Делает предсказание через ModelRegistry
- Рассчитывает risk_level (low/medium/high)
- Генерирует рекомендации на основе признаков
- Возвращает структурированный ответ

### service/main.py
FastAPI приложение.

Эндпоинты:
- GET /health — health check
- POST /predict — предсказание нагрузки
- GET /info — информация о модели

Особенности:
- Lifespan-контекст для загрузки модели при старте
- Pydantic-валидация входных/выходных данных
- Логирование запросов и ошибок
- Обработка исключений

### service/schemas.py
Pydantic схемы для API.

Классы:
- PredictionRequest — схема входных данных (X1-X8)
- PredictionResponse — схема ответа (heating_load, cooling_load, risk_level, recommendations, top_factors)

### utils/logging.py
Настройка логирования.

Функция setup_logger(log_path, name):
- Создаёт логгер с обработчиками (консоль + файл)
- Формат: время - уровень - сообщение
- Используется во всех модулях проекта

### service.py
Точка входа для запуска сервиса.

Запуск:
python -m src.service --host 127.0.0.1 --port 8000

Опции:
- --host — хост сервера (по умолчанию 127.0.0.1)
- --port — порт (по умолчанию 8000)
- --reload — автоперезагрузка при изменении кода

### train.py
Точка входа для обучения моделей.

Запуск:
python -m src.train

Что делает:
- Загружает данные через data/loader.py
- Строит препроцессор через features/preprocess.py
- Загружает конфиги моделей из experiment.yaml
- (Обучение вынесено в ноутбуки notebooks/)

## Как использовать

### Обучение
1. Запустите ноутбуки в notebooks/ для экспериментов
2. Или используйте python -m src.train для базового обучения

### Запуск сервиса
python -m src.service --host 0.0.0.0 --port 8000

### Тестирование
pytest tests/ -v

## Импорт модулей

Примеры импорта:

from src.config import load_yaml
from src.data.loader import load_and_prepare_data
from src.features.preprocess import build_preprocessor
from src.models.registry import ModelRegistry
from src.models.predictor import CoolingPredictor

## Важные замечания

1. Все модули используют относительные импорты внутри пакета
2. Пути вычисляются автоматически через pathlib
3. Конфигурация загружается из YAML файлов
4. Логирование настроено для всех компонентов
5. Код модульный и тестируемый (14 тестов в tests/)

Подробнее см. в основном README.md и report.md