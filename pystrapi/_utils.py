from typing import Any, Callable, Coroutine, TypeVar, Union


V = TypeVar('V')
D = TypeVar('D')


def getattr_safe(o: object, name: str, default: Any = '_UNKNOWN_') -> Any:
    """Wrap `getattr` with try/except to never raise exception.

    Usage

      >>> class A:
      ...     def __init__(self, x):
      ...         self.x = x
      >>> getattr_safe(A(x=1), 'x')
      1
      >>> getattr_safe(A(x=1), 'y')
      '_UNKNOWN_'
      >>> getattr_safe(A(x=1), 'y', 'my_default')
      'my_default'
    """
    try:
        return getattr(o, name, default)
    except Exception:
        return default


def getattrs_safe(o: object, *names: str, default: Any = '_UNKNOWN_') -> list:
    """Run `getattr_safe` on each attribute name and return results.

    Usage

      >>> class A:
      ...     def __init__(self, x, y):
      ...         self.x = x
      ...         self.y = y
      >>> getattrs_safe(A(x=1, y=2), 'x', 'y')
      [1, 2]
      >>> getattrs_safe(A(x=1, y=2), 'x', 'z')
      [1, '_UNKNOWN_']
      >>> getattrs_safe(A(x=1, y=2), 'x', 'z', default='my_default')
      [1, 'my_default']
    """
    return [getattr_safe(o, n, default) for n in names]


def run_safe(func: Callable[[], V], default: D) -> Union[V, D]:
    """Run function and return result. return `default` if failed."""
    try:
        return func()
    except Exception:
        return default


async def run_async_safe(func: Callable[[], Coroutine[Any, Any, V]], default: D) -> Union[V, D]:
    """Run async function and return result. return `default` if failed."""
    try:
        return await func()
    except Exception:
        return default
