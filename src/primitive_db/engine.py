from primitive_db.utils import load_metadata, save_metadata
from primitive_db.core import create_table, drop_table
from pathlib import Path


def run() -> None:
    print("database")
    print()
    commands_help = (
        "***Процесс работы с таблицей***\n"
        "Функции:\n"
        "<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу\n"
        "<command> list_tables - показать список всех таблиц\n"
        "<command> drop_table <имя_таблицы> - удалить таблицу\n"
        "<command> exit - выйти из программы\n"
        "<command> help - справочная информация"
    )
    print(commands_help)

    while True:
        command_raw = input("Введите команду: ").strip()
        command = command_raw.split(sep=" ", maxsplit= 2)
        if command[0] == "create_table":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            try:
                table_meta = {}
                for pair in command[2].split(' '):
                    for k, v in [pair.split(':')]:
                        table_meta[k.strip()] = v.strip()
                metadata = create_table(metadata, command[1], table_meta)
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    print(f'Таблица "{command[1]}" успешно создана со столбцами {command[2].replace(' ', ', ')}.')
            except:
                print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            print()
            continue
        if command[0] == "drop_table":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            try:
                metadata = drop_table(metadata, command[1])
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    print(f'Таблица "{command[1]}" удалена.')
            except:
                print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            print()
            continue
        if command[0] == "list_tables":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            for key in metadata:
                print(f"- {key}")
            print()
            continue
        if command[0] == "exit":
            break
        elif command[0] == "help":
            print(commands_help)
            print()
            continue
        else:
            print(f"Функции <{command[0]}> нет. Попробуйте снова.")
            print()
            pass

run()