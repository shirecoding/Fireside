# __all = ["TaskChain", "task_chain"]
# import logging
# from datetime import datetime
# from django.utils import timezone
# from pydantic import BaseModel

# from fireside.utils.task import task
# from typing import Any
# import queue

# logger = logging.getLogger(__name__)


# class TaskResult(BaseModel):
#     task_uid: str
#     started_on: datetime | None = None
#     ended_on: datetime | None = None

# class TaskChain(BaseModel):
#     tasks: list[TaskResult]  # task UIDs
#     event: Any  # first event


# @task(name="TaskChain", description="Chains several tasks in series")
# def task_chain(tasks: TaskChain) -> Any:

#     jobs = queue.Queue()
#     results = queue.Queue()

#     def on_success(job, connection, result, *args, **kwargs):
#         pass

#     def on_failure(job, connection, type, value, traceback):
#         pass

#     for t in tasks:
#         jobs.put(t)
