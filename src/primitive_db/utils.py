import json
from pathlib import Path

from primitive_db.constants import DATA_DIR


def load_metadata(path: str) -> dict:
    """Загружает метаданные таблиц, при отсутствии файла возвращает {}."""
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(path: str, data: dict) -> None:
    """Сохраняет метаданные таблиц в JSON-файл."""
    with open(path, "w") as file:
        json.dump(data, file)


def table_path(table_name: str) -> Path:
    """Возвращает путь к файлу с данными таблицы."""
    return Path(__file__).resolve().parent / DATA_DIR / f"{table_name}.json"


def load_table_data(table_name: str) -> list:
    """Загружает записи таблицы, при отсутствии файла возвращает []."""
    try:
        with open(table_path(table_name), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list) -> None:
    """Сохраняет записи таблицы, создавая папку с данными при необходимости."""
    path = table_path(table_name)
    path.parent.mkdir(exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file)
