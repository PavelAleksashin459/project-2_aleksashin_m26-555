import shlex
from pathlib import Path

from prettytable import PrettyTable

from primitive_db.constants import DATA_COMMANDS, META_FILE, TABLE_COMMANDS
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    matches,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import parse_set, parse_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

select_cache = create_cacher()


def print_help():
    """Выводит справку по доступным командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> "
        "values (<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def rows_to_table(rows: list) -> PrettyTable:
    """Строит PrettyTable из списка записей."""
    table = PrettyTable()
    if rows:
        table.field_names = rows[0].keys()
        for row in rows:
            table.add_row(row.values())
    return table


def handle_table_command(args: list, command_raw: str) -> None:
    """Выполняет команды create_table, drop_table и list_tables."""
    global select_cache
    command = args[0]
    meta_path = Path(__file__).with_name(META_FILE)
    metadata = load_metadata(meta_path)

    if command == "create_table":
        if len(args) <= 2:
            print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            return
        table_meta = {}
        for pair in args[2:]:
            name, typ = pair.split(":")
            table_meta[name] = typ
        metadata = create_table(metadata, args[1], table_meta)
        if metadata is not None:
            save_metadata(meta_path, metadata)
            save_table_data(args[1], [])
            select_cache = create_cacher()
            columns_text = ", ".join(
                f"{name}:{typ}" for name, typ in metadata[args[1]].items()
            )
            print(
                f'Таблица "{args[1]}" успешно создана '
                f"со столбцами: {columns_text}"
            )

    elif command == "drop_table":
        if len(args) != 2:
            print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")
            return
        metadata = drop_table(metadata, args[1])
        if metadata is not None:
            save_metadata(meta_path, metadata)
            select_cache = create_cacher()
            print(f'Таблица "{args[1]}" успешно удалена.')

    elif command == "list_tables":
        for key in metadata:
            print(f"- {key}")


def handle_data_command(args: list, head: str, where_text: str) -> None:
    """Выполняет команды insert, select, update, delete и info."""
    global select_cache
    command = args[0]
    table_name = args[1] if command in ("update", "info") else args[2]
    metadata = load_metadata(Path(__file__).with_name(META_FILE))
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    if command == "insert":
        values = [s.strip("(),") for s in args[4:]]
        table = insert(metadata, table_name, values)
        if table is not None:
            save_table_data(table_name, table)
            print(
                f'Запись с ID={table[-1]["ID"]} успешно добавлена '
                f'в таблицу "{table_name}".'
            )
        select_cache = create_cacher()

    elif command == "select":
        where_clause = parse_where(where_text) if where_text else None
        key = (table_name, where_text)
        rows = select_cache(
            key,
            lambda: select(load_table_data(table_name), where_clause)
        )
        print(rows_to_table(rows))

    elif command == "update":
        table = load_table_data(table_name)
        where_clause = parse_where(where_text)
        ids = [row["ID"] for row in table if matches(row, where_clause)]
        if not ids:
            print("Записи по условию не найдены.")
            return
        set_clause = parse_set(head.partition(" set ")[2])
        table = update(table, set_clause, where_clause)
        save_table_data(table_name, table)
        for record_id in ids:
            print(
                f'Запись с ID={record_id} в таблице "{table_name}" '
                f"успешно обновлена."
            )
        select_cache = create_cacher()

    elif command == "delete":
        table = load_table_data(table_name)
        where_clause = parse_where(where_text)
        ids = [row["ID"] for row in table if matches(row, where_clause)]
        if not ids:
            print("Записи по условию не найдены.")
            return
        table = delete(table, where_clause)
        if table is None:
            return
        save_table_data(table_name, table)
        for record_id in ids:
            print(
                f'Запись с ID={record_id} успешно удалена '
                f'из таблицы "{table_name}".'
            )
        select_cache = create_cacher()

    elif command == "info":
        columns_text = ", ".join(
            f"{name}:{typ}" for name, typ in metadata[table_name].items()
        )
        print(f"Таблица: {table_name}")
        print(f"Столбцы: {columns_text}")
        print(f"Количество записей: {len(load_table_data(table_name))}")


def run() -> None:
    """Запускает основной цикл обработки команд пользователя."""
    print("database")
    print_help()

    while True:
        command_raw = input(">>>Введите команду: ").strip()
        head, _, where_text = command_raw.partition(" where ")
        try:
            args = shlex.split(head)
            if not args:
                continue
            command = args[0]

            if command == "exit":
                break
            elif command == "help":
                print_help()
            elif command in TABLE_COMMANDS:
                handle_table_command(args, command_raw)
            elif command in DATA_COMMANDS:
                handle_data_command(args, head, where_text)
            else:
                print(f"Функции <{command}> нет. Попробуйте снова.")
        except (ValueError, IndexError):
            print(f"Некорректное значение: <{command_raw}>. Попробуйте снова.")


if __name__ == "__main__":
    run()
