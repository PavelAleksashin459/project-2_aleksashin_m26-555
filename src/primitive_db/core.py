from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data


@handle_db_errors
def create_table(metadata: dict, table_name: str, columns: dict) -> dict | None:
    """Добавляет в метаданные таблицу со столбцом ID и заданными столбцами."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None
    for value in columns.values():
        if value not in VALID_TYPES:
            raise ValueError(f"Некорректный тип: <{value}>. Попробуйте снова.")
    columns = {name: typ for name, typ in columns.items() if name != "ID"}
    metadata[table_name] = {"ID": "int", **columns}
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict, table_name: str) -> dict | None:
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    del metadata[table_name]
    return metadata


def convert(name: str, value: str, typ: str):
    """Преобразует значение к типу столбца."""
    if typ == "int" and value.lstrip("-").isdigit():
        return int(value)
    if typ == "bool" and value.lower() in ("true", "false"):
        return value.lower() == "true"
    if typ == "str":
        return value
    raise ValueError(f"значение <{value}> не подходит для столбца {name}:{typ}.")


@handle_db_errors
@log_time
def insert(metadata: dict, table_name: str, values: list) -> list | None:
    """Добавляет запись с новым ID и возвращает обновлённые данные таблицы."""
    schema = metadata[table_name]
    columns = [(name, typ) for name, typ in schema.items() if name != "ID"]
    if len(values) != len(columns):
        raise ValueError(
            "количество значений не совпадает с количеством столбцов."
        )

    table = load_table_data(table_name)
    new_id = max((row["ID"] for row in table), default=0) + 1
    row = {"ID": new_id}
    for (name, typ), value in zip(columns, values):
        row[name] = convert(name, value, typ)

    table.append(row)
    return table


def matches(row: dict, where_clause: dict) -> bool:
    """Проверяет, что запись удовлетворяет всем условиям where."""
    return all(row.get(key) == value for key, value in where_clause.items())


@log_time
def select(table_data: list, where_clause: dict | None = None) -> list:
    """Возвращает все записи или только подходящие под условие."""
    if where_clause is None:
        return table_data
    return [row for row in table_data if matches(row, where_clause)]


def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    """Обновляет поля в записях, подходящих под условие."""
    for row in table_data:
        if matches(row, where_clause):
            row.update(set_clause)
    return table_data


@confirm_action("удаление записи")
def delete(table_data: list, where_clause: dict) -> list:
    """Возвращает данные без записей, подходящих под условие."""
    return [row for row in table_data if not matches(row, where_clause)]
