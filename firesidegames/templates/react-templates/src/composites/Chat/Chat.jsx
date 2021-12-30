import React, { useState, useEffect, useContext } from "react";
import { webSocket } from "rxjs/webSocket";
import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";
import { UpdateGroup, User, Method, AppContext, ChatMessage } from "../../fsg";


const Chat = ({ messages, group, users, children }) => {
  /*
    Opens a websocket connection to url using user.uid and cookies.sessionid as query params
  */

  const { url, user, jwt, api } = useContext(AppContext)

  const [state, setState] = useState({
    messages: messages,
    users: users,
    webSocket: new webSocket(`${url}?jwt=${jwt}`)
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

  const onFriendRequest = (uid) => {
    console.log(`onFriendRequest: ${uid}`)
  }

  const onMail = (uid) => {
    console.log(`onMail: ${uid}`)
  }

  const onMessage = (uid) => {
    console.log(`onMessage: ${uid}`)
  }

  const onTextInput = (e) => {
    if (state.webSocket) {
      state.webSocket.next(
        ChatMessage({
          message: e,
          sender: user,
          receiver: group
        })
      )
    }
  }

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
            <ChatTextField onTextInput={onTextInput} />
          </div>
        </div>
      </div>
      <div className="col-3">
        <ChatUserList users={state.users} friends={friends} moderators={moderators}
        onFriendRequest={onFriendRequest} onMessage={onMessage} onMail={onMail}/>
      </div>
    </div>
  );
};

export default Chat;
