import pytest
from django_rq import get_scheduler

from fireside.models import Task, TaskPriority, TaskSchedule
from fireside.utils import function_to_import_path
from fireside.utils.task import task as task_decorator


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


def test_task_decorator(db):
    @task_decorator(name="Task From Decorator", description="Task From Decorator")
    def healthcheck(*args, **kwargs):
        pass

    task = Task.objects.get(name="Task From Decorator")
    assert task.name == "Task From Decorator"
    assert task.description == "Task From Decorator"


def test_task_schedule(task_schedule):

    # test queue
    assert task_schedule.get_queue().name == TaskPriority.LOW

    # test job in scheduler
    scheduler = get_scheduler()
    assert task_schedule.job_id in scheduler

    # test job
    assert task_schedule.get_job().id == task_schedule.job_id
