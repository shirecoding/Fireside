__all__ = ["JobDone"]

from .abstract import Event


class JobDone(Event):
    event: str = "fireside.events.tasks.JobDone"
    job_id: str
