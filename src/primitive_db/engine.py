import shlex
import json
from pathlib import Path

from primitive_db.core import create_table, drop_table, insert
from primitive_db.utils import load_metadata, save_metadata, save_table_data

META_FILE = "db_meta.json"

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

def print_help_for_tables():

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
        
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 


def parser(text: str) -> dict:
    args = shlex.split(text)
    if args[0] == 'insert':
        table = args[2]
        values = [s.replace(',', '').replace('(','').replace(')', '') for s in args[4:]]
        return args[0], table, values
    elif args[0] == 'select':
        table = args[2]
        if len(args) == 3:
            return args[0], table
        else:
            where_clause = {}
            where_clause[args[4]] = args[5]
        return args[0], table, where_clause
    elif args[0] == 'update':
        table = args[1]
        set_values = {}
        set_values[args[3]]= args[5]
        where_clause = {}
        where_clause[args[7]] = args[9]
        return args[0], table, set_values, where_clause
    elif args[0] == 'delete':
        table = args[2]
        where_clause = {}
        where_clause[args[4]] = args[5]
        return args[0], table, where_clause
    else:
        print(f"Функции <{args[0]}> нет. Попробуйте снова.")



def run() -> None:
    print("database")
    print()
    print_help()

    while True:
        command_raw = input(">>>Введите команду: ").strip()
        command = shlex.split(command_raw)
        if not command:
            continue
        elif command[0] == "create_table":
            meta_path = Path(__file__).with_name(META_FILE)
            metadata = load_metadata(meta_path)
            if len(command) > 2:
                table_meta = {}
                for pair in command[2:]:
                    name, typ = pair.split(':')
                    table_meta[name] = typ
                metadata = create_table(metadata, command[1], table_meta)
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    columns = metadata[command[1]]
                    columns_text = ", ".join(
                        f"{name}:{typ}" for name, typ in columns.items()
                    )
                    save_table_data(command[1], [])
                    print(
                        f'Таблица "{command[1]}" успешно создана '
                        f'со столбцами: {columns_text}'
                    )
            else:
                print(
                    f"Некорректное значение: <{command_raw}>. "
                    f"Попробуйте снова."
                )
            continue
        elif command[0] == "drop_table":
            meta_path = Path(__file__).with_name(META_FILE)
            metadata = load_metadata(meta_path)
            if len(command) == 2:
                metadata = drop_table(metadata, command[1])
                if metadata is not None:
                    save_metadata(meta_path, metadata)
                    print(f'Таблица "{command[1]}" успешно удалена.')
            else:
                print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            continue
        elif command[0] == "list_tables":
            meta_path = Path(__file__).with_name(META_FILE)
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

def operations_with_data():
    print("database")
    print()
    print_help_for_tables()

    while True:
        command_raw = input(">>>Введите команду: ").strip()
        command = parser(command_raw)
        if command[0] == 'insert':
            meta_path = Path(__file__).with_name(META_FILE)
            metadata = load_metadata(meta_path)
            table = insert(metadata[command[1]],command[1], command[2])
            save_table_data(command[1],table)
            continue
        if command[0] == "exit":
            break
        elif command[0] == "help":
            print_help_for_tables()
            continue
        else:
            print(f"Функции <{command[0]}> нет. Попробуйте снова.")


if __name__ == "__main__":
    operations_with_data()