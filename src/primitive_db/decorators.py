import time
from functools import wraps


def handle_db_errors(func):
    """Перехватывает ошибки базы данных и выводит сообщение вместо падения."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper


def confirm_action(action_name):
    """Запрашивает подтверждение [y/n] перед выполнением действия."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if answer.strip().lower() != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """Выводит время выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        duration = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """Создаёт функцию кэширования результатов по ключу."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает результат из кэша или вычисляет и сохраняет его."""
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result
