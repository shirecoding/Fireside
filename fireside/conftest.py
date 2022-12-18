import pytest
from django.core.management import call_command
from pydantic import BaseModel

from fireside.models import Task, TaskPreset, TaskPriority, TaskSchedule
from fireside.utils import function_to_import_path


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
        event=DummyInput(key="hello", value="world").dict(),
    )


@pytest.fixture
def task_schedule(db, task, task_preset) -> TaskSchedule:

    task_schedule = TaskSchedule.objects.create(
        task_preset=task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )
    assert TaskSchedule.objects.get(task_preset=task_preset).task_preset.task == task

    call_command("update_permissions")
    call_command("remove_stale_contenttypes")

    return task_schedule
