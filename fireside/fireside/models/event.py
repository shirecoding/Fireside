__all__ = ["Event", "EventHandler"]

from django.db import models

from fireside.models import Model, NameDescriptionModel


class Event(NameDescriptionModel):
    ...


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
