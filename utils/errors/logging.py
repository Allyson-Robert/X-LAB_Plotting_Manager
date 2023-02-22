import logging
import functools
from typing import Callable, Any
from utils.errors.errors import VocNotFoundError


def error_with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            func(*args, **kwargs)
        except VocNotFoundError as err:
            logger.error(f"Found error {err} calling {func.__name__}")

    return wrapper


def exceptions_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exc:
            import traceback
            logger.error(f"Found error {exc} calling {func.__name__}")
            logger.error(f"Reported trace: {traceback.format_exc()}")

            raise
    return wrapper
# TODO: https://stackoverflow.com/a/6307868 decorate class
