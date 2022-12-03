__all__ = ["function_to_import_path", "import_path_to_function", "cron_pretty"]

import inspect
from importlib import import_module
from typing import Callable

from cron_descriptor import ExpressionDescriptor


def function_to_import_path(func) -> str:
    return f"{inspect.getmodule(func).__name__}.{func.__name__}"


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
