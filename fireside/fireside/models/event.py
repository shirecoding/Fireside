__all__ = ["Event", "EventHandler"]

from django.db import models
from pydantic import BaseModel

from fireside.models import Model, NameDescriptionModel
from fireside.utils import import_path_to_function


class Event(NameDescriptionModel):
    mpath = models.CharField(
        max_length=256,
        blank=False,
        null=True,
        help_text="Import path to the `BaseModel` which represents the data type of the `Event`",
    )

    @property
    def base_model(self) -> BaseModel:
        return import_path_to_function(self.mpath)


class EventHandler(Model, NameDescriptionModel):
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        help_text="The task which will process the event.",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        help_text="The event which the event handler listens for.",
    )
