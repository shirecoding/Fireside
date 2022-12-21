__all__ = ["Event"]

from pydantic import BaseModel


class Event(BaseModel):
    event: str  # override accordingly (must be the import path of the event class)
