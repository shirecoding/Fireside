import logging
from typing import ClassVar

import pytest
from django.core.management import call_command

from fireside.models import Task, TaskPreset, TaskPriority, TaskSchedule
from fireside.utils import Protocol, ProtocolDict, function_to_import_path

logger = logging.getLogger(__name__)


class PMessage(Protocol):
    protocol: ClassVar[str] = "pmessage"
    text: str


def logging_task(**protocols) -> ProtocolDict:
    logger.debug(protocols)
    return protocols


@pytest.fixture
def task(db) -> Task:
    return Task.objects.create(
        name="Logging Task",
        description="Logging Task",
        fpath=function_to_import_path(logging_task),
    )


@pytest.fixture
def task_preset(db, task) -> TaskPreset:
    protocols = PMessage(text="The quick brown fox jumps over the lazy dog.")
    task_preset = TaskPreset.objects.create(
        name="Log Messages",
        task=task,
        protocols=protocols.as_kwargs(jsonify=True),
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
