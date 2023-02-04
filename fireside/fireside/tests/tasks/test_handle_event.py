import pytest
from pydantic import ValidationError

from fireside.utils.event import handle_event
from fireside.utils.task import get_task_result


def test_handle_event(
    db,
    chat_message_event,
    chat_message_event_handler,
    logging_task,
    text_message,
):
    assert chat_message_event_handler.event == chat_message_event
    assert chat_message_event_handler.task == logging_task

    task_logs = handle_event(chat_message_event, text=text_message.text)
    result = get_task_result(task_logs[0])

    assert result == text_message.dict()


def test_handle_event_invalid_input(
    db,
    chat_message_event,
    chat_message_event_handler,
    logging_task,
    text_message,
):
    assert chat_message_event_handler.event == chat_message_event
    assert chat_message_event_handler.task == logging_task

    with pytest.raises(ValidationError):
        handle_event(chat_message_event, invalid_kwarg=10)

    # test partial kwargs
    task_logs = handle_event(
        chat_message_event, text=text_message.text, invalid_kwarg=10
    )
    result = get_task_result(task_logs[0])

    assert result == text_message.dict()
