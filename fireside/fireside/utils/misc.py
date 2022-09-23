__all__ = ["get_function_import_path"]

import inspect


def get_function_import_path(func) -> str | None:
    m = inspect.getmodule(func)
    if m is not None:
        return f"{m.__name__}.{func.__name__}"
    return None
