# primitive-db

Сборка и установка:

```bash
uv build
uv tool install --force dist/primitive_db-0.1.0-py3-none-any.whl
```

Запуск:

```bash
database
```

## Управление таблицами

Метаданные таблиц хранятся в `db_meta.json`. Допустимые типы столбцов: `int`, `str`, `bool`. При создании таблицы столбец `ID:int` добавляется автоматически.

Команды:

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ..` — создать таблицу
- `list_tables` — показать список всех таблиц
- `drop_table <имя_таблицы>` — удалить таблицу
- `help` — справочная информация
- `exit` — выйти из программы

Пример:

```text
>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.

>>>Введите команду: list_tables
- users

>>>Введите команду: drop_table users
Таблица "users" успешно удалена.

>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.
```

## CRUD-операции

Данные каждой таблицы хранятся в отдельном файле `data/<имя_таблицы>.json`. Значение `ID` генерируется автоматически, его не нужно передавать в `insert`. Все остальные поля обязательны. Строковые значения пишутся в кавычках.

Команды:

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись
- `select from <имя_таблицы>` — прочитать все записи
- `select from <имя_таблицы> where <столбец> = <значение>` — прочитать записи по условию
- `update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>` — обновить запись
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись
- `info <имя_таблицы>` — вывести информацию о таблице

Пример:

```text
>>>Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

>>>Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei | 28  |    True   |
+----+--------+-----+-----------+

>>>Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.

>>>Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".

>>>Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0
```

Демонстрация:

[![asciicast](https://asciinema.org/a/JfsuxMqh9SEKbSik.svg)](https://asciinema.org/a/JfsuxMqh9SEKbSik)

