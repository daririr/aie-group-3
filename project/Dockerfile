# Используем легкий образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем uv (менеджер пакетов)
RUN pip install uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем все зависимости
RUN uv sync --frozen

# Копируем весь код проекта
COPY . .

# Открываем порт 8000 для API
EXPOSE 8000

# Настраиваем проверку работоспособности (health check)
# Проверяем доступность эндпоинта /health каждые 30 секунд
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Запускаем FastAPI сервер
# uvicorn — ASGI сервер, src.main:app — путь к приложению
# --host 0.0.0.0 — слушаем все интерфейсы
# --port 8000 — порт
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]