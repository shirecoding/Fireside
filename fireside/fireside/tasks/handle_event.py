__all = ["handle_event"]

import logging
from typing import Iterable

from cachetools.func import ttl_cache
from rq.job import Job

from fireside.models import Event, EventHandler
from fireside.utils.task import task

logger = logging.getLogger(__name__)


@ttl_cache(ttl=600)
def get_event_handlers(event: Event | str) -> Iterable[Event]:
    return EventHandler.objects.filter(
        event=event if isinstance(event, Event) else Event.objects.get(name=event)
    )


@task(
    name="HandleEvent", description="Run `EventHandlers` which listens for the event."
)
def handle_event(event: Event | str, **kwargs) -> list[Job]:
    return [e.task.delay(**kwargs) for e in get_event_handlers(event)]
