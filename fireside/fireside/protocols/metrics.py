__all__ = ["PError", "PMetric"]

from datetime import datetime

from .defs import Protocol


class PError(Protocol):
    protocol: str = "perror"
    klass: str = "fireside.protocols.metrics.PError"
    type: str
    value: str
    traceback: str | None = None


class PMetric(Protocol):
    protocol: str = "pmetric"
    klass: str = "fireside.protocols.metrics.PMetric"
    started_on: datetime | None = None
    completed_on: datetime | None = None
    error: PError | None = None
