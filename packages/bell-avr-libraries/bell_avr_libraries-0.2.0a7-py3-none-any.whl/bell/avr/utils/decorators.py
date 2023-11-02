"""
These are [function decorators](https://www.programiz.com/python-programming/decorator)
helpful for MQTT message callbacks.
"""

import functools
import time
from typing import Any, Callable, Optional

from loguru import logger


def try_except(reraise: bool = False) -> Callable:
    """
    Function decorator that acts as a try/except block around the function.

    Effectively equivalent to:

    ```python
    try:
        func()
    except Exception as e:
        print(e)
    ```

    This will log any exceptions to the console.

    Example:

    ```python
        from bell.avr.utils import decorators

        @decorators.try_except
        def assemble_hil_gps_message(self) -> None:
            ...
    ```

    Additionally, there is the `reraise` argument, which can be set to `True` to raise
    any exceptions that are encountered. This is helpful if you still want exceptions
    to propagate up, but log them.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Unexpected exception in {func.__name__}")
                if reraise:
                    raise e from e

        return wrapper

    return decorator


def async_try_except(reraise: bool = False) -> Callable:
    """
    Same as `try_except()` function, just for async functions.

    Example:

    ```python
        from bell.avr.utils import decorators

        @decorators.async_try_except()
        async def connected_status_telemetry(self) -> None:
            ...
    ```
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Unexpected exception in {func.__name__}")
                if reraise:
                    raise e from e

        return wrapper

    return decorator


def run_forever(
    period: Optional[float] = None, frequency: Optional[float] = None
) -> Callable:
    """
    Function decorator that acts as a while: True block around the function, that
    runs every `period` seconds, or `frequency` times per second.
    Either `period` or `frequency` must be set.

    Effectively equivalent to:

    ```python
    while True:
        time.sleep(period)
        func()
    ```

    Example:

    ```python
        from bell.avr.utils import decorators

        @decorators.run_forever(frequency=5)
        def read_data(self) -> None:
            ...
    ```
    """

    if frequency is not None:
        period = 1 / frequency

    assert period is not None

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            while True:
                time.sleep(period)
                func(*args, **kwargs)

        return wrapper

    return decorator
