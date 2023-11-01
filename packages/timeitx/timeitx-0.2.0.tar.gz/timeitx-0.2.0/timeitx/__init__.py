import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Optional


def timeitX(name: Optional[str], logger: Optional[logging.Logger]) -> Callable[..., Any]:
    """
    A decorator that logs the execution time of a function, both for synchronous and asynchronous functions.

    :param name: An optional string representing the name of the function being logged.
    :type name: str
    :return: A decorator function.
    """
    logger = logger if logger else logging.getLogger("timeitX")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def async_execution_timer(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper for asynchronous function execution time logging.
            """
            start_time = time.perf_counter()
            logger.info(f"Started execution of {name if name else func.__name__}")
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                elapsed_time_sec = round(end_time - start_time, 6)
                elapsed_time_ms = round(elapsed_time_sec * 1000, 3)
                fields = {
                    "function_name": name if name else func.__name__,
                    "elapsed_time_sec": elapsed_time_sec,
                    "elapsed_time_ms": elapsed_time_ms,
                }
                logger.info(
                    f"Finished execution of {name if name else func.__name__}. Time elapsed: {elapsed_time_sec} seconds ({elapsed_time_ms} ms)",
                    extra=fields,
                )

        @wraps(func)
        def sync_execution_timer(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper for synchronous function execution time logging.
            """
            start_time = time.perf_counter()
            logger.info(f"Started execution of {name if name else func.__name__}")
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                elapsed_time_sec = round(end_time - start_time, 6)
                elapsed_time_ms = round(elapsed_time_sec * 1000, 3)
                fields = {
                    "function_name": name if name else func.__name__,
                    "elapsed_time_sec": elapsed_time_sec,
                    "elapsed_time_ms": elapsed_time_ms,
                }
                logger.info(
                    f"Finished execution of {name if name else func.__name__}. Time elapsed: {elapsed_time_sec} seconds ({elapsed_time_ms} ms)",
                    extra=fields,
                )

        return async_execution_timer if asyncio.iscoroutinefunction(func) else sync_execution_timer

    return decorator
