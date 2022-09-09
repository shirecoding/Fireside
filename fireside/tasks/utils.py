__all__ = ["register_task"]

import inspect
from tasks.models import TaskDefinition


def register_task(name="", description=""):
    """
    Decorator used to register any function as a task.
    Uses type hints to create the schema for the `inputs` field.

    To ensure that tasks are discovered and registered, import tasks in AppConfig.ready

    TODO:
        - add schema based on type hints of function
    """

    def decorator(f):
        TaskDefinition.objects.update_or_create(
            fpath=f"{inspect.getmodule(f).__name__}.{f.__name__}", defaults={"name": name, "description": description}
        )

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator
