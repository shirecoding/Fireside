import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

import { UpdateGroup, User, Method } from "../../fsg";

const Chat = ({ url, messages, user, group, users, onTextInput }) => {

  const [state, setState] = useState({
    messages: messages,
    users: users,
    webSocket: new webSocket(url)
  });

  useEffect(() => {

    const systemUser = User({uid: "system"})

    // subscribe to web socket
    state.webSocket.subscribe(
      // on message
      (payload) => {

        // ChatMessage
        if (payload.type === 'ChatMessage') {
          setState((state) => {
            return {
              ...state,
              messages: [...state.messages, {user: payload.sender, message: payload.message}],
            };
          });
        }

        // UpdateGroup
        else if (payload.type === 'UpdateGroup') {
          setState((state) => {
            return {
              ...state,
              users: payload.users,
            };
          });
        }

      },
      // error
      (e) => {
        console.log('failed to connect ...')
        setState((state) => {
          return {
            ...state,
            messages: [...state.messages, {user: systemUser, message: "connection failed"}]
          };
        });
      },
      // end
      (e) => {
        console.log('connection completed ...')
        setState((state) => {
          return {
            ...state,
            messages: [...state.messages, {user: systemUser, message: "connection closed"}]
          };
        });
      }
    );

    // send group update on load
    state.webSocket.next(UpdateGroup({
      sender: user,
      receiver: group,
      method: Method.add,
      users: [user]
    }))

    // clean up
    return () => {
      console.log("closing websocket ...");
      state.webSocket.complete();
    }

  }, [group, user, state.webSocket]);

  return (
    <div className="row h-100">
      <div className="col-9">
        <div className="row mb-2 h-100">
          <ChatWindow messages={state.messages}/>
        </div>
        <div className="row">
          <ChatTextField onTextInput={(e) => onTextInput(state, e)} />
        </div>
      </div>
      <div className="col-3">
        <ChatUserList users={state.users} />
      </div>
    </div>
  );
};

export default Chat;
