def create_table(metadata: dict, table_name: str, columns: dict) -> None:
    if table_name in metadata:
        print(f"Таблица {table_name} уже создана, удалите таблицу или переименуйте ее")
    else:
        for value in columns.values():
            if value is int:
                pass
            elif value is str:
                pass
            elif value is bool:
                pass
            else:
                print("Допустимы только типы int, str, bool")
                break

        metadata += {table_name: columns}
        return metadata

def drop_table(metadata: dict, table_name: str):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует")
    else:
        del metadata[table_name]
        return metadata
        