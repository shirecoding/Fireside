__all__ = ["TaskCompleted", "task_completed_event"]

from datetime import datetime

from pydantic import BaseModel

from fireside.utils.event import register_event


class TaskCompleted(BaseModel):
    task_uid: str
    completed_on: datetime


task_completed_event = register_event(
    "TaskCompleted",
    TaskCompleted,
    description="`Event` when a `Task` is completed.",
)
