import inspect
from typing import Any, Coroutine, TypeVar, Union


V = TypeVar("V", bound="Any")


async def value(val: Union[V, Coroutine[Any, Any, V]]) -> V:
    """
    Return the given value. await if it's awaitable.
    """
    if inspect.isawaitable(val):
        return await val  # type: ignore
    return val  # type: ignore
