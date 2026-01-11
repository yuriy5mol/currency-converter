"""
Модуль для работы с файловым хранилищем курсов валют.
"""
import json
import os
import time
from typing import Any


RATES_FILE = "currency_rates.json"


def save_to_file(data: dict[str, Any]) -> None:
    """Сохраняет данные в JSON файл."""
    with open(RATES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_from_file() -> dict[str, Any]:
    """Читает данные из JSON файла."""
    with open(RATES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def file_exists() -> bool:
    """Проверяет, существует ли файл с курсами."""
    return os.path.exists(RATES_FILE)


def get_file_age_hours() -> float:
    """Возвращает возраст файла в часах."""
    file_mtime = os.path.getmtime(RATES_FILE)
    return (time.time() - file_mtime) / 3600
