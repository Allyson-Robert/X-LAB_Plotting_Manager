import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import functools
from typing import Callable, Any
from utils import constants

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


def with_logging(func: Callable[..., Any], log_level: int = 10) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # FIXME: Logger name is magic string
        logger = logging.getLogger(constants.LOG_NAME)

        logger.log(log_level, f"Calling {func.__qualname__}")
        value = func(*args, **kwargs)
        logger.log(log_level, f"Finished calling {func.__qualname__}")

        return value
    return wrapper

def decorate_abc_with_debug_logging(cls, list_of_methods, log_level):
    for function_to_wrap in list_of_methods:
        setattr(
            cls,
            function_to_wrap,
            with_logging(cls.__dict__[function_to_wrap], log_level=log_level)
        )
