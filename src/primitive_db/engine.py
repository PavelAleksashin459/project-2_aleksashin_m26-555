from primitive_db.utils import load_metadata, save_metadata
from primitive_db.core import create_table, drop_table
from pathlib import Path
import shlex

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def run() -> None:
    print("database")
    print()
    print_help()

    while True:
        command_raw = input(">>>Введите команду: ").strip()
        command = shlex.split(command_raw)
        if not command:
            continue
        if command[0] == "create_table":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            try:
                table_meta = {}
                for pair in command[2:]:
                    name, typ = pair.split(':')
                    table_meta[name] = typ
                metadata = create_table(metadata, command[1], table_meta)
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    columns = metadata[command[1]]
                    columns_text = ", ".join(f"{name}:{typ}" for name, typ in columns.items())
                    print(f'Таблица "{command[1]}" успешно создана со столбцами: {columns_text}')
            except:
                print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            continue
        if command[0] == "drop_table":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            try:
                metadata = drop_table(metadata, command[1])
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    print(f'Таблица "{command[1]}" успешно удалена.')
            except:
                print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            continue
        if command[0] == "list_tables":
            meta_path = Path(__file__).with_name("db_meta.json")
            metadata = load_metadata(meta_path)
            for key in metadata:
                print(f"- {key}")
            continue
        if command[0] == "exit":
            break
        elif command[0] == "help":
            print_help()
            continue
        else:
            print(f"Функции <{command[0]}> нет. Попробуйте снова.")

if __name__ == "__main__":
    run()