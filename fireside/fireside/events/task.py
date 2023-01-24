__all__ = ["TaskCompleted"]

from pydantic import BaseModel

from fireside.utils.event import register_event


class TaskCompleted(BaseModel):
    task_uid: str


register_event(
    "TaskCompleted",
    TaskCompleted,
    description="`Event` for when a `Task` is completed.",
)
