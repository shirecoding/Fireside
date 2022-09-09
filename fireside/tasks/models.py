__all__ = ["Task", "TaskDefinition"]

from fireside.models import Model, ActivatableModel
from django.db import models
import importlib


class TaskDefinition(Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    fpath = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        null=False,
        help_text="Path to the function to be run (eg. path.to.function)",
    )

    def __str__(self):
        return f"{self.name} ({self.fpath})"


def default_task_inputs():
    return {"args": "", "kwargs": {}}


class Task(Model, ActivatableModel):
    """
    TODO:
        - Replace inputs JSONField with SchemaJSONField (validate with task_definitions.<task>.schema)
        - Add cron
        - Display cron as readable string "every saturday 10 pm"
        - Store results, errors
        - Add action
    """

    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=256, default="")
    inputs = models.JSONField(
        default=default_task_inputs, help_text="JSON containing the `args` and `kwargs` for `task`"
    )
    definition = models.ForeignKey("TaskDefinition", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    def run(self):
        xs = self.definition.fpath.split(".")
        getattr(importlib.import_module(".".join(xs[:-1])), xs[-1])(*self.inputs["args"], **self.inputs["kwargs"])
