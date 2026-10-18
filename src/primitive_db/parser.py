def parse_value(raw: str):
    """Преобразует текстовое значение в str (в кавычках), bool или int."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    return int(raw)


def parse_condition(text: str) -> dict:
    """Разбирает условие вида 'столбец = значение' в словарь."""
    column, sep, value = text.partition("=")
    if not sep or not column.strip():
        raise ValueError(text)
    return {column.strip(): parse_value(value)}


def parse_where(text: str) -> dict:
    """Разбирает условие where в словарь {столбец: значение}."""
    return parse_condition(text)


def parse_set(text: str) -> dict:
    """Разбирает перечень присваиваний set через запятую в словарь."""
    result = {}
    for part in text.split(","):
        result.update(parse_condition(part))
    return result
