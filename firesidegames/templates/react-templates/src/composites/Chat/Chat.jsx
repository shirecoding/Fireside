import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

const Chat = ({ url, messages, users, onTextInput }) => {

  const [state, setState] = useState({
    messages: messages,
    users: users,
    webSocket: new webSocket(url)
  });

  useEffect(() => {

    // subscribe to web socket
    state.webSocket.subscribe(
      // success
      ({type, message, sender}) => {
        if (type === 'DirectMessage') {
          setState((state) => {
            return {
              ...state,
              messages: [...state.messages, {user: sender, message: message}],
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
