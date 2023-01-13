__all__ = ["Event", "EventHandler"]

from django.db import models

from fireside.models import Model, NameDescriptionModel, Task
from fireside.utils import import_path_to_function


class Event(NameDescriptionModel):
    """
    Use `fireside.utils.event.register_event` to create `Event`s
    """

    data_klass = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        help_text="Import path to the event data class (pydantic).",
    )

    def get_data_klass(self):
        return import_path_to_function(self.data_klass)


class EventHandler(Model, NameDescriptionModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        help_text="The task which will process the event.",
    )
    event = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        help_text="The event which the event handler listens for.",
    )
