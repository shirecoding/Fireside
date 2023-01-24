__all__ = ["register_event"]


from pydantic import BaseModel

from fireside.models import Event
from fireside.utils import function_to_import_path


def register_event(name: str, base_model: BaseModel, description: str = "") -> Event:
    return Event.objects.update_or_create(
        name=name,
        defaults={
            "description": description,
            "mpath": function_to_import_path(base_model),
        },
    )[0]
