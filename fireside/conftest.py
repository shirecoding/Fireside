import logging

import pytest
from django.core.management import call_command
from pydantic import BaseModel

from fireside.models import (
    Event,
    EventHandler,
    Task,
    TaskPreset,
    TaskPriority,
    TaskSchedule,
)
from fireside.utils import JSONObject, function_to_import_path
from fireside.utils.event import register_event

logger = logging.getLogger(__name__)


class Message(BaseModel):
    text: str


def log_message(*, message: Message) -> JSONObject:
    logger.debug(message)
    return {"message": message}


def capitalize_message(*, message: Message) -> JSONObject:
    return {"message": Message(text=message.text.title())}


def reverse_message(*, message: Message) -> JSONObject:
    return {"message": Message(text=message.text[::-1])}


@pytest.fixture
def text_message() -> Message:
    return Message(text="The quick brown fox jumps over the lazy dog.")


@pytest.fixture
def logging_task(db) -> Task:
    return Task.objects.create(
        name="Logging Task",
        description="Logging Task",
        fpath=function_to_import_path(log_message),
    )


@pytest.fixture
def capitalize_message_task(db) -> Task:
    return Task.objects.create(
        name="Capitalize Task",
        description="Capitalize Task",
        fpath=function_to_import_path(capitalize_message),
    )


@pytest.fixture
def reverse_message_task(db) -> Task:
    return Task.objects.create(
        name="Reverse Task",
        description="Reverse Task",
        fpath=function_to_import_path(reverse_message),
    )


@pytest.fixture
def logging_task_preset(db, logging_task, text_message) -> TaskPreset:
    task_preset = TaskPreset.objects.create(
        name="Log Messages Task Preset",
        task=logging_task,
        kwargs={
            "message": text_message.dict()
        },  # `TaskPreset` kwargs is a JSONField and needs to be JSON serializable
    )
    assert TaskPreset.objects.get(task=logging_task) == task_preset

    return task_preset


@pytest.fixture
def logging_task_schedule(db, logging_task_preset) -> TaskSchedule:

    task_schedule = TaskSchedule.objects.create(
        task_preset=logging_task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )
    assert TaskSchedule.objects.get(task_preset=logging_task_preset) == task_schedule

    call_command("update_permissions")
    call_command("remove_stale_contenttypes")

    return task_schedule


@pytest.fixture
def chat_message_event(db) -> Event:
    event = register_event(
        "ChatMessageEvent", Message, description="A Chat Message Event"
    )

    assert event.name == "ChatMessageEvent"
    assert event.description == "A Chat Message Event"
    assert event.get_data_klass() == Message

    return event


@pytest.fixture
def chat_message_event_handler(db, chat_message_event, logging_task) -> EventHandler:
    ev_handler = EventHandler.objects.create(
        task=logging_task,
        event=chat_message_event,
        name="ChatMessageEventHandler",
        description="Logs `ChatMessageEvent`s to debug console",
    )

    assert ev_handler.name == "ChatMessageEventHandler"
    assert ev_handler.description == "Logs `ChatMessageEvent`s to debug console"
    assert ev_handler.task == logging_task
    assert ev_handler.event == chat_message_event

    return ev_handler
