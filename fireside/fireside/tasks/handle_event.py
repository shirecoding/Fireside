__all = ["handle_event"]

import logging
from typing import Iterable

from fireside.models import Event, EventHandler
from fireside.utils.task import task

logger = logging.getLogger(__name__)


def get_event_handlers(event: Event | str) -> Iterable[Event]:
    return EventHandler.objects.filter(
        event=event if isinstance(event, Event) else Event.objects.get(name=event)
    )


@task(
    name="HandleEvent", description="Run `EventHandlers` which listens for the event."
)
def handle_event(event: Event | str, **kwargs) -> None:
    for e in get_event_handlers(event):
        e.task.delay(**kwargs)
