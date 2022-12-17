## Events

- `Event` has a `type` and `data`
- They are the inputs and ouputs of tasks
- They may be created by `Producers` (eg. Websocket)
- They may be sent to a `TaskChain` (Sequence of tasks)
- Priority of the event overrides the task's default priority

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
    data: Json  # should overwrite with pydantic model for introspection
```

## Tasks

See `fireside.models.Task` and `fireside.models.TaskSchedule`

- `Task`s input and output `Event`s. This allows compatible tasks to be chained
- `Task`s are queued and processed by rq workers
- `Task`s may be scheduled by created a `TaskSchedule`

## Task Stream

- `Task`s may be chained together to form a `TaskChain`
- `TaskChain` is itself a `Task` which is proccessed by an rq worker

```python
class TaskChainPayload(BaseModel):
    task_uids: list[str]

class TaskChain(Event):
    type: 'TaskChain'
    data: TaskChainPayload

from fireside.utils.task import task


@task(name="TaskChain", description="Chains a series of Tasks")
def task_chain(ev: TaskChain):
    task_uids = ev.data.task_uids

    rx.of(task_uids).pipe(
        ops.reduce(lambda t: Task.objects.get(uid=t))
    )
```

- A `Producer` (eg. Websocket route) creates an `Event` and submits it to the `EventCoordinator` with the requested `task_chain_uid`.
- The `EventCoordinator` gets the `TaskChain` from the database, and calls the first `Task` in the chain.
- The output of each task is fed into the next task in the chain as input.

## Event Coordinator Task

The `EventCoordinator` shuttles events to tasks via `Event.destination`.
