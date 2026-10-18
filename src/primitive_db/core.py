from primitive_db.utils import load_table_data


def create_table(metadata: dict, table_name: str, columns: dict) -> None:
    '''
        Добавляет table_name и columns
    '''
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return
    else:
        for value in columns.values():
            if value == "int":
                pass
            elif value == "str":
                pass
            elif value == "bool":
                pass
            else:
                print(f"Некорректный тип: <{value}>. Попробуйте снова.")
                return
        if "ID" in columns:
            metadata[table_name] = columns
        else:
            columns = {"ID": "int", **columns}
            metadata[table_name] = columns
        return metadata

def drop_table(metadata: dict, table_name: str):
    '''
        Удаляет таблицу
    '''
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    else:
        del metadata[table_name]
        return metadata

def convert(value: str, typ: str):
    '''
        Преобразует типы
    '''
    if typ == "int":
        return int(value)
    if typ == "bool":
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        raise ValueError(value)
    return value

def insert(metadata: dict, table_name: str, values: list) -> list | None:
    '''
        Вставляет данные в таблицу
    '''
    table = load_table_data(table_name)
    columns = [(name, typ) for name, typ in metadata.items() if name != "ID"]
    if len(values) != len(columns):
        print("Ошибка: количество значений не совпадает с количеством столбцов.")
        return None

    new_id = max((row["ID"] for row in table), default=0) + 1
    row = {"ID": new_id}
    for (name, typ), value in zip(columns, values):
        try:
            row[name] = convert(value, typ)
        except ValueError:
            print(f"Ошибка: значение <{value}> не подходит для столбца {name}:{typ}.")
            return None

    table.append(row)
    return table

def matches(row: dict, where_clause: dict) -> bool:
    return all(row.get(key) == value for key, value in where_clause.items())

def select(table_data: list, where_clause: dict | None = None) -> list:
    if where_clause is None:
        return table_data
    return [row for row in table_data if matches(row, where_clause)]

def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    for row in table_data:
        if matches(row, where_clause):
            row.update(set_clause)
    return table_data

def delete(table_data: list, where_clause: dict) -> list:
    return [row for row in table_data if not matches(row, where_clause)]
