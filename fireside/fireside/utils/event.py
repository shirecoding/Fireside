__all__ = ["register_event", "handle_event"]

import logging
from typing import TYPE_CHECKING, Iterable

from cachetools.func import ttl_cache
from pydantic import BaseModel

from fireside.models.event import Event, EventHandler
from fireside.utils import function_to_import_path

if TYPE_CHECKING:
    from fireside.models.task import TaskLog

logger = logging.getLogger(__name__)


def register_event(name: str, base_model: BaseModel, description: str = "") -> Event:
    return Event.objects.update_or_create(
        name=name,
        defaults={
            "description": description,
            "mpath": function_to_import_path(base_model),
        },
    )[0]


@ttl_cache(ttl=600)
def get_event_handlers(event: Event | str) -> Iterable[Event]:
    return EventHandler.objects.filter(
        event=event if isinstance(event, Event) else Event.objects.get(name=event)
    )


def handle_event(event: Event | str, **kwargs) -> list["TaskLog"]:

    # validate kwargs (throws ValidationError)
    event.base_model.parse_obj(kwargs)

    return [e.task.delay(**kwargs) for e in get_event_handlers(event)]
