__all__ = ["events", "publish_event", "start_listening"]

import json
import logging
import threading

from django_rq import get_connection
from reactivex.subject import Subject

from fireside.utils import import_path_to_function

from .abstract import Event
from .defs import EVENT_CHANNEL

con = get_connection()
logger = logging.getLogger(__name__)

events = Subject()


def publish_event(ev: Event, channel: str | None = None):
    con.publish(channel or EVENT_CHANNEL, ev.json())  # jsonify


def start_listening(channel: str | None = None) -> Subject:
    """
    Needs to be started only ONCE on the process which subscribes to events
    """
    channel = channel or EVENT_CHANNEL
    pubsub = con.pubsub()
    pubsub.subscribe(channel)

    logger.info(f"Listening for events on {channel}")

    def _loop():
        for item in pubsub.listen():
            try:
                if item["type"] == "message":
                    # deserialize json
                    data = json.loads(item["data"].decode("utf-8"))
                    events.on_next(import_path_to_function(data["event"])(**data))
            except Exception:
                logger.exception(f"Failed to deserialize event {item}")

    threading.Thread(target=_loop, daemon=True).start()

    return events
