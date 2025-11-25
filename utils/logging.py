import logging
import functools
from typing import Callable, Any
from implementations.utils import constants

DEBUG = 10
DEBUG_DATA_TYPE = 11
DEBUG_DATA_PROCESSOR = 12
DEBUG_PLOTTER = 13
DEBUG_WORKER = 14
DEBUG_GUI = 15

class ConsoleLogging:
    # FIXME: Logger name is magic string
    def __init__(self):
        self.logger = logging.getLogger(constants.LOG_NAME)

    def console_print(self, level=10, message=None):
        self.logger.log(level, message)


def with_logging(func=None, *, log_level: int = 10):
    """
    Logging decorator usable as:
        @with_logging
        @with_logging()
        @with_logging(log_level=...)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(constants.LOG_NAME)
            logger.log(log_level, f"Calling {func.__qualname__}")
            value = func(*args, **kwargs)
            logger.log(log_level, f"Finished calling {func.__qualname__}")
            return value
        return wrapper

    # CASE 1: @with_logging  → func is the decorated function
    if callable(func):
        return decorator(func)

    # CASE 2: @with_logging(...) → func is None, return real decorator
    return decorator

from types import FunctionType

def decorate_class_with_logging(
    log_level: int = 10,
    include: set[str] | None = None,
    exclude: set[str] | None = None,
):
    """
    Class decorator that wraps explicitly defined *methods* on a class
    with `with_logging`, without touching Qt signals or other descriptors.

    - Only items in `cls.__dict__` that are real functions (or class/staticmethods)
      are wrapped.
    - By default, public methods (no leading underscore) are wrapped.
    - You can narrow/adjust behaviour with `include` / `exclude`.
    """

    def decorator(cls):
        for name, attr in cls.__dict__.items():
            # unwrap classmethod / staticmethod
            is_classmethod = isinstance(attr, classmethod)
            is_staticmethod = isinstance(attr, staticmethod)
            func = attr.__func__ if (is_classmethod or is_staticmethod) else attr

            # only wrap *real* functions, not pyqtSignal, properties, etc.
            if not isinstance(func, FunctionType):
                continue

            # skip dunder + private-ish names
            if name.startswith("__") and name.endswith("__"):
                continue
            if name.startswith("_"):
                continue

            # optional filters
            if include is not None and name not in include:
                continue
            if exclude is not None and name in exclude:
                continue

            # your existing with_logging(func, log_level=...)
            wrapped_func = with_logging(func, log_level=log_level)

            # re-wrap as classmethod/staticmethod if needed
            if is_classmethod:
                wrapped_attr = classmethod(wrapped_func)
            elif is_staticmethod:
                wrapped_attr = staticmethod(wrapped_func)
            else:
                wrapped_attr = wrapped_func

            setattr(cls, name, wrapped_attr)

        return cls

    return decorator
