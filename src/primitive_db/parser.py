def parse_value(raw: str):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    return int(raw)


def parse_condition(text: str) -> dict:
    column, sep, value = text.partition("=")
    if not sep or not column.strip():
        raise ValueError(text)
    return {column.strip(): parse_value(value)}


def parse_where(text: str) -> dict:
    return parse_condition(text)


def parse_set(text: str) -> dict:
    result = {}
    for part in text.split(","):
        result.update(parse_condition(part))
    return result