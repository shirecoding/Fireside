## Events

```python
from pydantic import BaseModel, Field, Json
from typing import Literal
from uuid import UUID, uuid4

class Event(BaseModel):
    priority: Literal['low', 'medium', 'high'] = 'low'
    origin: str | None = None
    destination: str | None = None
    uid: UUID = Field(default_factory=uuid4)
    type: str
    payload: Json  # should overwrite with pydantic model for introspection
```

## Tasks

- Tasks take `Event` as input ONLY.
- Priority of the event overrides the task's priority

## Task Stream

```python
class TaskStreamPayload(BaseModel):
    task_uids: list[str]

class TaskStream(Event):
    type: 'TaskStream'
    payload: TaskStreamPayload
```

```python
from fireside.models import ActivatableModel, Model

class TaskStream(Model, ActivatableModel):
    # tasks in order

```

- A `Producer` (eg. Websocket route) creates an `Event` and submits it to the `EventCoordinator` with the requested `task_stream_uid`.
- The `EventCoordinator` gets the `TaskStream` from the database, and calls the first `Task` in the stream.
- The output of each task is fed into the next task in the stream as input.

## Event Coordinator Task

The `EventCoordinator` shuttles events to tasks via `Event.destination`.
