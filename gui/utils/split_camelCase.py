import re


def split_camel_case(camel_case) -> list[str]:
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', camel_case)