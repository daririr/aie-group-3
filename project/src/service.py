#!/usr/bin/env python3
"""
Запуск:
    python -m src.service
    uv run python -m src.service
Или напрямую через uvicorn:
    uv run uvicorn src.service.main:app --host 127.0.0.1 --port 8000
"""

import sys
import argparse
from pathlib import Path

# Добавляем корень проекта в PATH для импортов
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Запуск сервиса предсказания нагрузки на охлаждение"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Хост для сервера"
    )
    parser.add_argument("--port", type=int, default=8000, help="Порт для сервера")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Включить автоперезагрузку при изменении кода",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Формируем команду для uvicorn
    reload_flag = "--reload" if args.reload else ""
    cmd = f"uvicorn src.service.main:app --host {args.host} --port {args.port} {reload_flag}"

    print(f"Запуск команды: {cmd}")

    # Запускаем uvicorn как подпроцесс
    import subprocess

    result = subprocess.run(cmd.split(), cwd=PROJECT_ROOT)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
