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
        