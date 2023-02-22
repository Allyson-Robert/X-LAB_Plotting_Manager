from types import FunctionType


def methods(cls):
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
