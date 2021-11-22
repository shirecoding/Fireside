import React from "react";
import Chat from "../Chat";
import { ChatMessage } from "../../fsg";

const Gameroom = ({ url, messages, user, group, users }) => {

  const onTextInput = (chatState, e) => {
    if (chatState.webSocket) {
      chatState.webSocket.next(
        ChatMessage({
          message: e,
          sender: user,
          receiver: group
        })
      )
    }
  }

  return (
    <Chat url={url} messages={messages} user={user} group={group} users={users} onTextInput={onTextInput}/>
  )
};

export default Gameroom;
