import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

const Chat = ({ url, messages, users }) => {

  const [state, setState] = useState({messages: [], users: []});

  useEffect(() => {

    const webSocketSubject = new webSocket(url);

    // subscribe to web socket
    webSocketSubject.subscribe(
      // success
      (e) => {
        console.log('connected ...')
        setState((state) => {
          return { ...state, messages: [...state.messages, e] };
        });
      },
      // error
      (e) => {
        console.log('failed to connect ...')
        setState((state) => {
          return { ...state, messages: [...state.messages, {user: "connection", message: "connection failed"}] };
        });
      },
      // end
      (e) => {
        console.log('connection completed ...')
        setState((state) => {
          return { ...state, messages: [...state.messages, {user: "connection", message: "connection closed"}] };
        });
      }
    );

    // clean up
    return () => {
      console.log("closing websocket ...");
      webSocketSubject.complete();
    }

  }, []);

  const onTextInput = () => {
    console.log('onTextInput')
  }

  return (
    <div className="row">
      <div className="col-9">
        <div className="row">
          <ChatWindow messages={messages} />
        </div>
        <div className="row">
          <ChatTextField onTextInput={onTextInput} />
        </div>
      </div>
      <div className="col-3">
        <ChatUserList users={users} />
      </div>
    </div>
  );
};

export default Chat;
