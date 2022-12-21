import logging

import pytest
from django.core.management import call_command

from fireside.models import Task, TaskPreset, TaskPriority, TaskSchedule
from fireside.protocols import Protocol, ProtocolDict
from fireside.utils import function_to_import_path

logger = logging.getLogger(__name__)


class PMessage(Protocol):
    protocol: str = "pmessage"
    text: str


def logging_task(*, pmessage: PMessage) -> ProtocolDict:
    logger.debug(pmessage)
    return pmessage.as_kwargs()


@pytest.fixture
def pmessage() -> PMessage:
    return PMessage(text="The quick brown fox jumps over the lazy dog.")


@pytest.fixture
def task(db) -> Task:
    return Task.objects.create(
        name="Logging Task",
        description="Logging Task",
        fpath=function_to_import_path(logging_task),
    )


@pytest.fixture
def task_preset(db, task, pmessage) -> TaskPreset:
    task_preset = TaskPreset.objects.create(
        name="Log Messages",
        task=task,
        protocols=pmessage.as_kwargs(jsonify=True),
    )
    assert TaskPreset.objects.get(task=task) == task_preset

    return task_preset


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
