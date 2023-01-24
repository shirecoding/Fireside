from fireside.utils.task import get_task_result


def test_handle_event(
    db,
    capfd,
    chat_message_event,
    chat_message_event_handler,
    logging_task,
    text_message,
):
    from fireside.tasks.handle_event import (
        handle_event,  # need to import here as it requires db connection
    )

    assert chat_message_event_handler.event == chat_message_event
    assert chat_message_event_handler.task == logging_task

    jobs = handle_event(chat_message_event, text=text_message.text)
    result = get_task_result(jobs[0])

    assert result == text_message.dict()
