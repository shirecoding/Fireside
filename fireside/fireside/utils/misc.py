__all__ = ["function_to_import_path", "import_path_to_function"]

import inspect
from importlib import import_module
from typing import Callable


def function_to_import_path(func) -> str:
    return f"{inspect.getmodule(func).__name__}.{func.__name__}"


def import_path_to_function(fpath: str) -> Callable:
    xs = fpath.split(".")
    return getattr(import_module(".".join(xs[:-1])), xs[-1])
