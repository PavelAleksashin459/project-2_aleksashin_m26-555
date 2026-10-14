import json


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
