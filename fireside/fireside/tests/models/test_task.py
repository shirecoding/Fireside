import pytest
from django_rq import get_scheduler

from fireside.models import Task, TaskPriority, TaskSchedule
from fireside.utils import function_to_import_path


def dummy_task(*args, **kwargs):
    pass


@pytest.fixture
def task(db) -> Task:
    return Task.objects.create(
        name="Dummy Task",
        description="Dummy Task",
        fpath=function_to_import_path(dummy_task),
    )


@pytest.fixture
def task_schedule(db, task) -> TaskSchedule:

    task_schedule = TaskSchedule.objects.create(
        task=task,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
        inputs={},
    )
    assert TaskSchedule.objects.get(task=task).task == task

    return task_schedule


def task_task_decorator():
    task = Task.objects.get(name="Healthcheck")
    assert task.name == "Healthcheck"


def test_task_schedule(task_schedule):

    # test queue
    assert task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert task_schedule.job_id in scheduler

    # test job
    assert task_schedule.get_job().id == task_schedule.job_id
