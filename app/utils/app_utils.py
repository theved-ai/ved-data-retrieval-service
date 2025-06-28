from typing import Callable, TypeVar, Union, Awaitable


def ensure(predicate: Callable[[], bool], exception: Exception) -> None:
    """
    Evaluate predicate(); if it returns False, raise the given exception.
    """
    if not predicate():
        raise exception

async def ensure_async(predicate: Callable[[], Awaitable[bool]], exception: Exception) -> None:
    """
    Evaluate predicate()in async; if it returns False, raise the given exception.
    """
    if not await predicate():
        raise exception


T = TypeVar("T")

def execute_if_or_else(
        predicate: bool,
        if_fn: Callable[[], Union[T, None]],
        else_fn: Callable[[], Union[T, None]]
) -> T:
    """
    Lazily execute one of two callables based on the boolean predicate.
    """
    return if_fn() if predicate else else_fn()


async def execute_try_catch_async(
        try_fn: Callable[[], Awaitable[T]],
        catch_fn: Callable[[Exception], Exception]
) -> T:
    """
    Executes the async try_fn. If it raises, catch_fn(exc) is called
    to produce a new Exception which is then raised.
    """
    try:
        return await try_fn()
    except Exception as e:
        new_exc = catch_fn(e)
        raise new_exc from e