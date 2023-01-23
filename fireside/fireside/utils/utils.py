__all__ = [
    "function_to_import_path",
    "import_path_to_function",
    "cron_pretty",
    "generate_uuid",
    "remove_falsy",
    "remove_none",
]

import inspect
import uuid
from functools import lru_cache
from importlib import import_module
from typing import Callable, Generator, Iterator, TypeVar, cast

from cron_descriptor import ExpressionDescriptor

_T = TypeVar("_T")


@lru_cache
def function_to_import_path(func) -> str:
    return f"{inspect.getmodule(func).__name__}.{func.__name__}"


@lru_cache
def import_path_to_function(fpath: str) -> Callable:
    xs = fpath.split(".")
    return getattr(import_module(".".join(xs[:-1])), xs[-1])


def cron_pretty(cron: str) -> str:
    """Returns a human readable representation of a cron string

    Args:
        cron: Cron string (eg. * * * * *)
    Returns:
        Human readable representation of a cron string (eg. Every minute)
    """
    try:
        return str(ExpressionDescriptor(cron))
    except Exception as e:
        return str(e)


def generate_uuid() -> str:
    return uuid.uuid4().hex


def remove_none(obj: _T) -> _T:
    if isinstance(obj, dict):
        return cast(
            _T,
            type(obj)(
                (remove_none(k), remove_none(v))
                for k, v in obj.items()
                if k is not None and v is not None
            ),
        )

    if isinstance(obj, (list, tuple, set)):
        return cast(_T, type(obj)(remove_none(x) for x in obj if x is not None))

    if isinstance(obj, (Generator, Iterator)):
        return cast(_T, (remove_none(x) for x in obj if x is not None))

    return obj


def remove_falsy(obj: _T) -> _T:
    if isinstance(obj, dict):
        return cast(
            _T,
            type(obj)(
                (remove_falsy(k), remove_falsy(v)) for k, v in obj.items() if k and v
            ),
        )

    if isinstance(obj, (list, tuple, set)):
        return cast(_T, type(obj)(remove_falsy(x) for x in obj if x))

    if isinstance(obj, (Generator, Iterator)):
        return cast(_T, (remove_falsy(x) for x in obj if x))

    return obj
