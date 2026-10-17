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

def insert(metadata: dict, table_name: str, values: list) -> None:
    table = load_table_data(table_name)
    if len(values) == len(metadata) -1:
        keys_list = list(metadata.items())
        converted_values = {}
        i = 0
        for key in keys_list[1:]:
            if key[1] == "int":
                try:
                    converted_values[key[0]] = int(values[i])
                except ValueError:
                    print(f"Ошибка: значение <{values[i]}> не подходит для столбца {key[0]}:{key[1]}.")
                    return None
            elif key[1] == "str":
                try:
                   converted_values[key[0]] = str(values[i])
                except ValueError:
                    print(f"Ошибка: значение <{values[i]}> не подходит для столбца {key[0]}:{key[1]}.")
                    return None
            elif key[1] == "bool":
                try:
                    converted_values[key[0]] = bool(values[i])
                except ValueError:
                    print(f"Ошибка: значение <{values[i]}> не подходит для столбца {key[0]}:{key[1]}.")
                    return None
            i += 1
        new_id = max((int(k) for k in table), default=0) + 1
        table[new_id] = converted_values
        return table
    else: 
        print("Ошибка: количество значений не совпадает с количеством столбцов.")
        return None

def select(table_data:dict, where_clause = None):
    if where_clause == None:
        table_data
    else:
        filtered_table = {item for item in table_data.items() if where_clause in item.value()}
        return filtered_table

def update(table_data:dict, set_clause:dict, where_clause:dict):
    for item in table_data.items():
        for value in item.values():
            if value == where_clause:
                item[set_clause.key()] = set_clause.value()
    return table_data

def delete(table_data, where_clause):
    for item in table_data.items():
        for value in item.values():
            if value == where_clause:
                del table_data[item]
    return table_data
