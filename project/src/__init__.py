"""
src – сервисная часть проекта предиктивной оценки нагрузки на охлаждение.

Используется:
- как FastAPI-приложение (uvicorn src.main:app);
- как библиотека для загрузки моделей, конфигурации и логики инференса.
"""

from . import main, predictor, config

__all__ = ["main", "predictor", "config"]
__version__ = "0.1.0"
