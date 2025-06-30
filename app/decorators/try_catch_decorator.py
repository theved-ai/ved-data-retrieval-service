import functools
from typing import Callable
from app.utils.app_utils import execute_try_catch_async

def try_catch_wrapper(logger_fn: Callable[[Exception], None]):
    def decorator(func):
        @functools.wraps(func)
        async def wrapped(self, *args, **kwargs):
            async def try_fn():
                return await func(self, *args, **kwargs)

            return await execute_try_catch_async(
                try_fn=try_fn,
                catch_fn=logger_fn
            )
        return wrapped
    return decorator
