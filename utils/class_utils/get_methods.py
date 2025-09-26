# Deprecating
from types import FunctionType
import warnings


def get_methods(cls):
    warnings.warn("Function will be removed in stable release. Will be replaced by 'get_class_methods'", DeprecationWarning)
    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
