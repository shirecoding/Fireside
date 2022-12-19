__all__ = [
    "Protocol",
    "PError",
    "PMetric",
]

from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel


class Protocol(BaseModel):
    protocol: ClassVar[str]  # override accordingly (reserved keyword, use lowercase)

    def as_kwargs(self) -> dict[str, "Protocol"]:
        return {self.protocol: self}


class PError(Protocol):
    protocol: ClassVar[str] = "perror"
    type: str
    value: str
    traceback: str | None = None


class PMetric(Protocol):
    protocol: ClassVar[str] = "pmetric"
    started_on: datetime | None = None
    completed_on: datetime | None = None
    error: PError | None = None
