__all__ = ["register_event"]

from pydantic import BaseModel

from fireside.models import Event
from fireside.utils import function_to_import_path


def register_event(name: str, data_klass: BaseModel, description: str = "") -> Event:
    return Event.objects.update_or_create(
        name=name,
        defaults={
            "data_klass": function_to_import_path(data_klass),
            "description": description,
        },
    )[0]
