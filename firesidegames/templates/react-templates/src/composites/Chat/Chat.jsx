import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

import { UpdateGroup, User, Method } from "../../fsg";

const Chat = ({ url, messages, user, group, users, onTextInput, children }) => {
  /*

    - Opens a websocket connection to url using user.uid and cookies.sessionid as query params
  */

  const [state, setState] = useState({
    messages: messages,
    users: users,
    webSocket: new webSocket(`${url}?username=${user.uid}&session=${document.cookie.sessionid}`)
  });

  useEffect(() => {

    const systemUser = User({uid: "system"})

    // subscribe to web socket
    state.webSocket.subscribe(
      // success
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

  const friends = []
  const moderators = []

  return (
    <div className="row vh-100">
      <div className="col-9">
        <div className="d-flex flex-column" style={{height: "calc(100% - 100px)"}}>
          <div className="flex-column overflow-scroll" style={{height: "20rem"}}>
            {children}
          </div>
          <div className="flex-column flex-grow-1 my-2">
            <ChatWindow messages={state.messages}/>
          </div>
          <div className="flex-column">
            <ChatTextField onTextInput={(e) => onTextInput(state, e)} />
          </div>
        </div>
      </div>
      <div className="col-3">
        <ChatUserList users={state.users} friends={friends} moderators={moderators} />
      </div>
    </div>
  );
};

export default Chat;
