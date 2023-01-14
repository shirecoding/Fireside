def test_handle_event(db, chat_message_event, text_message):
    from fireside.tasks.handle_event import (
        handle_event,  # need to import here as it requires db connection
    )

    handle_event(chat_message_event, message=text_message)
