import pytest
from django_rq import get_scheduler
from pydantic import BaseModel

from fireside.models import Task, TaskPreset, TaskPriority, TaskSchedule
from fireside.utils import function_to_import_path
from fireside.utils.task import task as task_decorator


class DummyInput(BaseModel):
    key: str
    value: str


class DummyOutput(BaseModel):
    key: str
    value: str


def dummy_task(ev: DummyInput) -> DummyOutput:
    return DummyOutput(**ev)


@pytest.fixture
def task(db) -> Task:
    return Task.objects.create(
        name="Dummy Task",
        description="Dummy Task",
        fpath=function_to_import_path(dummy_task),
    )


@pytest.fixture
def task_preset(db, task) -> TaskPreset:
    return TaskPreset.objects.create(
        name="Dummy Task Hello World",
        task=task,
        event=DummyInput(key="hello", value="world"),
    )


@pytest.fixture
def task_schedule(db, task, task_preset) -> TaskSchedule:

    task_schedule = TaskSchedule.objects.create(
        task_preset=task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )
    assert TaskSchedule.objects.get(task_preset=task_preset).task == task

    return task_schedule


def test_task_decorator(db):
    @task_decorator(name="Task From Decorator", description="Task From Decorator")
    def healthcheck(event):
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
