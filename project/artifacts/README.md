# Артефакты проекта

В этой папке хранятся артефакты, полученные в процессе работы над проектом Energy Efficiency Prediction.

## Структура

artifacts/
├── models/              # Обученные модели
│   ├── best_model_manifest.json   # Манифест финальной модели
│   ├── Stacking_Y1.pkl            # Модель для Y1 (Heating Load)
│   └── Stacking_Y2.pkl            # Модель для Y2 (Cooling Load)
├── metrics/             # Метрики и результаты экспериментов
│   ├── model_selection.json       # Сравнение моделей
│   └── results_summary.csv        # Сводная таблица метрик
├── figures/             # Визуализации и графики
│   ├── eda/                       # Графики EDA
│   │   ├── correlation_matrix.png
│   │   ├── target_distributions.png
│   │   ├── top_features_vs_Y2.png
│   │   ├── X6_boxplots.png
│   │   ├── X8_boxplots.png
│   │   └── Y1_vs_Y2.png
│   └── 01_exp/                    # Графики экспериментов
│       └── models_comparison_r2.png
└── logs/                # Логи сервиса и обучения
    └── service.log                # Логи FastAPI сервиса

## Модели

Финальная модель: StackingRegressor

Артефакты:
- Stacking_Y1.pkl — модель для предсказания Heating Load (Y1)
- Stacking_Y2.pkl — модель для предсказания Cooling Load (Y2)
- best_model_manifest.json — манифест с описанием модели

Метрики на тестовой выборке:

Таргет	      R²	      RMSE	   MAE
Y1 (Heating)	0.9988	0.3592	0.2657
Y2 (Cooling)	0.9909	0.9055	0.6056

Метрики на валидационной выборке:

Таргет	      R²	      RMSE	   MAE
Y1 (Heating)	0.9990	0.2986	0.2130
Y2 (Cooling)	0.9965	0.5446	0.4074

Архитектура:
- Base models: LinearRegression, RandomForest, CatBoost
- Final estimator: LinearRegression
- CV: 5-fold
- Preprocessing: StandardScaler + OneHotEncoder

## Метрики

results_summary.csv
Сводная таблица со всеми метриками (MAE, RMSE, R²) для всех моделей:
- LinearRegression
- RandomForest
- CatBoost
- Stacking (финальная)

model_selection.json
JSON с результатом выбора модели:
{
  "selected_model": "Stacking",
  "selection_criteria": "max_mean_R2_valid",
  "validation_scores": {
    "Stacking": 0.9978,
    "CatBoost": 0.9976,
    "RandomForest": 0.9896,
    "LinearRegression": 0.9347
  }
}

## Визуализации

EDA (Exploratory Data Analysis):
- correlation_matrix.png — матрица корреляций признаков
- target_distributions.png — распределение целевых переменных Y1 и Y2
- top_features_vs_Y2.png — топ признаки vs Cooling Load
- X6_boxplots.png — влияние ориентации здания (X6) на нагрузку
- X8_boxplots.png — влияние распределения остекления (X8)
- Y1_vs_Y2.png — зависимость между Heating и Cooling Load

Эксперименты:
- models_comparison_r2.png — сравнение моделей по R²

## Логи

service.log — логи работы FastAPI сервиса (запросы, ошибки, время ответа)

## Важные замечания

1. Не коммитьте большие файлы!
   - Модели .pkl уже закоммичены (они небольшие ~1-5 MB)
   - Логи не должны превышать 1 MB
   - Для крупных артефактов используйте внешние хранилища

2. Артефакты для демонстрации:
   - Финальные модели уже находятся в models/
   - Метрики в metrics/ готовы для проверки
   - Графики в figures/ используются в отчёте

3. Воспроизведение:
   - Все артефакты можно пересоздать, запустив ноутбуки в notebooks/
   - Модели переобучаются через python -m src.train

Подробнее о моделях и экспериментах см. в report.md