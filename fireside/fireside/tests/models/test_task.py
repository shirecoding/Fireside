import logging

import pytest
from django_rq import get_scheduler

from fireside.models.task import Task, TaskPriority, TaskStatus
from fireside.utils import JSONObject
from fireside.utils.task import get_task_result
from fireside.utils.task import task as task_decorator

logger = logging.getLogger(__name__)


def test_task_decorator(db):
    @task_decorator(name="DoNothing", description="This task does nothing")
    def do_nothing(**kwargs) -> JSONObject:
        return {**kwargs}

    task = Task.objects.get(name="DoNothing")
    assert task.name == "DoNothing"
    assert task.description == "This task does nothing"


def test_task_schedule(logging_task_schedule):

    # test queue
    assert logging_task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert logging_task_schedule.job_id in scheduler

    # test job
    assert logging_task_schedule.get_job().id == logging_task_schedule.job_id


def test_task_preset(logging_task_preset, text_message):
    assert logging_task_preset.run() == text_message.dict()


def test_task_enqueue(logging_task, text_message):

    # test task success
    task_log = logging_task.enqueue(**text_message.dict())
    assert get_task_result(task_log) == text_message.dict()

    # test task failure
    task_log = logging_task.enqueue(invalid_arg="this will cause an error")

    with pytest.raises(Exception):
        get_task_result(task_log)

    assert task_log.status == TaskStatus.FAILED
    assert task_log.result is None
    assert task_log.traceback
