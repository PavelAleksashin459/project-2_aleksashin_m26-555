import json
from pathlib import Path


def load_metadata(path: str) -> dict:
    '''
        Загружает таблицу с метаданными
    '''
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print('Error: file was not found.')
        return {}

def save_metadata(path: str, data: dict) -> None:
    '''
        Сохраняет таблицу с метаданными
    '''
    with open(path, "w") as file:
        json.dump(data, file)

def load_table_data(table_name:str) -> list:
    '''
        Загружает данные из таблицы
    '''
    path = Path(__file__).resolve().parent/'data'/f"{table_name}.json"
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_table_data(table_name:str, data: list) -> None:
    '''
        Сохраняет таблицу c данными
    '''
    path = Path(__file__).resolve().parent/'data'/f"{table_name}.json"
    path.parent.mkdir(exist_ok=True)
    with open(path, "w") as file:
        json.dump(data, file)