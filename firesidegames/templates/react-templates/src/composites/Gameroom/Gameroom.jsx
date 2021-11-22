import React, { useState, useEffect } from "react";
import Chat from "../Chat";
import { GlobalMessage, ChatMessage, UpdateGroup, Group, User } from "../../fsg";

const Gameroom = ({ url, messages, user, group, users }) => {

  const onTextInput = (chatState, e) => {
    if (chatState.webSocket) {
      chatState.webSocket.next(
        new GlobalMessage({message: e, sender: user})
      )
    }
  }

  return (
    <Chat url={url} messages={messages} user={user} group={group} users={users} onTextInput={onTextInput}/>
  )
};

export default Gameroom;
