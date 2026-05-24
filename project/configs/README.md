# Конфигурационные файлы

В этой папке хранятся настройки проекта Energy Efficiency Prediction.

## Файлы

### data.yaml
Настройки данных:
- путь к датасету ENB2012_data.csv
- разделители (точка с запятой, запятая)
- схема данных: какие колонки числовые, категориальные, целевые

### experiment.yaml
Параметры обучения:
- random_state и test_size
- настройки препроцессинга (StandardScaler, OneHotEncoder)
- гиперпараметры моделей (LinearRegression, RandomForest, CatBoost, Stacking)

### serving.yaml
Настройки сервиса:
- путь к артефактам
- пороги риска (low/medium/high)
- хост и порт сервера

### .env.example
Шаблон переменных окружения (без реальных значений):
- ARTIFACTS_PATH
- CONFIGS_PATH
- LOG_LEVEL

## Важно

- Не коммитьте файл .env с реальными значениями!
- .env автоматически игнорируется через .gitignore
- Все конфиги загружаются автоматически через src/config.py

Подробнее о работе с конфигурацией см. в main README.md