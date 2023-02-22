import logging
import functools
from typing import Callable, Any


def with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logger.info(f"Finished calling {func.__name__}")

        return value
    return wrapper
