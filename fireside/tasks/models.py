__all__ = ["Task", "register_task"]

from fireside.models import Model
from django.db import models
import inspect

task_definitions = {}


def task_choices():
    for k, d in task_definitions.items():
        yield (
            k,
            f"{d['name']} ({k})",
        )


def register_task(name=""):
    """
    Decorator used to register any function as a task.
    Uses function type hints to create the schema for the `inputs` field

    TODO:
        - add schema based on type hints of function
    """

    def decorator(f):
        # register function
        fpath = f"{inspect.getmodule(f).__name__}.{f.__name__}"
        task_definitions[fpath] = {
            "fpath": fpath,
            "name": name,
            "schema": None,
        }

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


@register_task(name="Default Inputs")
def default_inputs():
    return {"args": "", "kwargs": {}}


class Task(Model):
    """
    TODO:
        - Replace inputs JSONField with SchemaJSONField
        - Add cron
        - Display cron as readable string "every saturday 10 pm"
        - Add deactivate_on, activate_on (mixin? with is_activated, is_deactivated)
    """

    name = models.CharField(max_length=128, blank=False, null=False, help_text="Name of this task")
    description = models.TextField(max_length=256, default="")
    inputs = models.JSONField(
        default=default_inputs, help_text="JSON containing the `args` and `kwargs` parameters for the function `task`"
    )
    task = models.CharField(
        max_length=128,
        choices=task_choices(),
        blank=False,
        null=False,
        help_text="Path to the function to be run (eg. path.to.function)",
    )

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def register_task(cls, *args, **kwargs):
        return register_task(*args, **kwargs)
