__all__ = ["TaskCompleted", "task_completed_event"]

from pydantic import BaseModel

from fireside.utils.event import register_event


class TaskCompleted(BaseModel):
    task_uid: str
    task_log_uid: str


# TODO: event handler which listens for this task and triggers another task will cause another TaskCompleted event leading to an endless chain
task_completed_event = register_event(
    "TaskCompleted",
    TaskCompleted,
    description="`Event` when a `Task` is completed.",
)
