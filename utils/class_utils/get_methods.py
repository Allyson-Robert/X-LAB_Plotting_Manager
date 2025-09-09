from types import FunctionType


def get_methods(cls):
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
