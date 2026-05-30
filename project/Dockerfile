FROM python:3.14-slim

LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="API для предсказания энергоэффективности зданий"

# Рабочая директория
WORKDIR /app

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ARTIFACTS_PATH=/app/artifacts \
    CONFIGS_PATH=/app/configs \
    LOG_LEVEL=info

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Копируем зависимости и устанавливаем их
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Копируем исходный код
COPY . .

# Устанавливаем проект
RUN uv sync --frozen --no-dev

# Создаём папку для логов (если нет)
RUN mkdir -p /app/artifacts/logs

# Порт
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Запуск
CMD ["uv", "run", "uvicorn", "src.service.main:app", "--host", "0.0.0.0", "--port", "8000"]