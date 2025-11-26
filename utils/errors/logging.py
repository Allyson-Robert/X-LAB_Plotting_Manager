"""
Logging wrappers that report errors to the user interface without crashing it.

These decorators are provided for future use and are not yet used anywhere
in the codebase.
"""
import logging
import functools
from typing import Callable, Any
from utils.errors.errors import VocNotFoundError


def error_with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    """
    Wrap a function so that :class:`VocNotFoundError` is logged and suppressed.

    Parameters
    ----------
    func:
        Callable to execute.
    logger:
        Logger instance used to record the error.

    Returns
    -------
    Callable[..., Any]
        A wrapper that calls ``func`` and logs any :class:`VocNotFoundError`
        instead of propagating it.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            func(*args, **kwargs)
        except VocNotFoundError as err:
            logger.error(f"Found error {err} calling {func.__name__}")

    return wrapper


def exceptions_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    """
    Decorator that logs and re-raises any exception raised by ``func``.

    Parameters
    ----------
    func:
        Callable to wrap.
    logger:
        Logger instance used to record the exception and traceback.

    Returns
    -------
    Callable[..., Any]
        A wrapper that logs the exception details before re-raising them.
    """
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
