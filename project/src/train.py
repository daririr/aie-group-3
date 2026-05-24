#!/usr/bin/env python3
"""
Точка входа для обучения моделей.

Запуск:
    python -m src.train
    uv run python -m src.train
"""

import sys
import logging
from pathlib import Path

# Добавляем корень проекта в PATH для импортов
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logging import setup_logger
from src.data.loader import load_and_prepare_data
from src.features.preprocess import build_preprocessor
from src.config import load_yaml, ARTIFACTS_DIR, CONFIGS_DIR

# Исправлено: используем ARTIFACTS_DIR вместо ARTIFACTS_ROOT
LOG_PATH = ARTIFACTS_DIR / "logs" / "train.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logger = setup_logger(str(LOG_PATH), name="train")


def main():
    logger.info("=== Запуск обучения ===")

    # 1. Загрузка данных
    logger.info("Загрузка данных...")
    X_train, X_test, y_train, y_test, num_cols, cat_cols, target_cols = (
        load_and_prepare_data()
    )
    logger.info(f"Данные загружены: train={len(X_train)}, test={len(X_test)}")

    # 2. Построение препроцессора
    logger.info("Построение препроцессора...")
    preprocessor = build_preprocessor(num_cols, cat_cols)

    # 3. Загрузка конфигурации моделей
    exp_cfg = load_yaml("experiment.yaml")
    models_cfg = exp_cfg["models"]

    # 4. Здесь должна быть логика обучения (вынесена из ноутбука)
    # Для простоты — заглушка, которую можно расширить
    logger.info("Обучение моделей...")
    logger.info("Модели: " + ", ".join(models_cfg.keys()))

    # 5. Сохранение артефактов (если нужно)
    logger.info(f"Артефакты сохранены в: {ARTIFACTS_DIR}")

    logger.info("=== Обучение завершено ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
