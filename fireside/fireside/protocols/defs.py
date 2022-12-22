from __future__ import annotations

__all__ = ["ProtocolDict", "TaskTree"]

import json
from typing import ForwardRef, Union

from pydantic import BaseModel

from fireside.utils import JSONObject

from .abstract import Protocol

ProtocolDict = dict[str, Union[Protocol, JSONObject]]

TaskTree = ForwardRef("TaskTree")


class TaskTree(BaseModel):
    task_uid: str
    job_id: str | None = (
        None  # used to get the `ProtocolDict` result of the completed task
    )
    children: list[TaskTree] = []

    class Config:
        json_encoders = {
            TaskTree: lambda t: json.dumps(t.dict()),
        }


TaskTree.update_forward_refs()
