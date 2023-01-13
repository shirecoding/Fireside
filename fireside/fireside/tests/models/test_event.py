def test_event_handler(db, chat_message_event, chat_message_event_handler):

    assert chat_message_event_handler.event == chat_message_event
