import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

import {ChatMessage, UpdateGroup, Group, User} from "../../fsg";

const Chat = ({ url, messages, user, group, users, onTextInput }) => {

  const [state, setState] = useState({
    messages: messages,
    users: users,
    webSocket: new webSocket(url)
  });

  useEffect(() => {

    // subscribe to web socket
    state.webSocket.subscribe(
      // on message
      (payload) => {

        // ChatMessage
        if (payload.type === 'ChatMessage') {
          setState((state) => {
            return {
              ...state,
              messages: [...state.messages, {user: payload.sender.uid, message: payload.message}],
            };
          });
        }

        // UpdateGroup
        else if (payload.type === 'UpdateGroup') {
          setState((state) => {
            return {
              ...state,
              users: [...payload.users.map((uid) => ({name: uid})), {name: user}],
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
            messages: [...state.messages, {user: "connection", message: "connection failed"}]
          };
        });
      },
      // end
      (e) => {
        console.log('connection completed ...')
        setState((state) => {
          return {
            ...state,
            messages: [...state.messages, {user: "connection", message: "connection closed"}]
          };
        });
      }
    );

    // send group update on load
    const sender = new User({uid: user})
    const receiver = new Group({uid: group})
    const msg = new UpdateGroup({
      sender: sender,
      receiver: receiver,
      users: [...users.map(({name}) => name), user]
    })
    state.webSocket.next(msg)

    // clean up
    return () => {
      console.log("closing websocket ...");
      state.webSocket.complete();
    }

  }, []);

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
