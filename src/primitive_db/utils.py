import json

def load_metadata(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Error: file was not found.')
        

def save_metadata(path: str, data: dict) -> None:
    with open(path, "w") as file:
        json.dump(data, file)
