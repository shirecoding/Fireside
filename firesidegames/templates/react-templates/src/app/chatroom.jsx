import React from 'react';
import ReactDOM from 'react-dom';
import {ChatMessage, Group, User} from "../fsg";
import Chat from "../composites/Chat";


const Chatroom = ({user, users, group, messages, url}) => {

  const onTextInput = (state, e) => {
    if (state.webSocket) {
      state.webSocket.next(new ChatMessage({
        sender: user,
        receiver: group,
        message: e,
      }))
    }
  }

  return (
    <div className="container-fluid" style={{height: '500px'}}>
      <Chat user={user} users={users} group={group} messages={messages} url={url} onTextInput={onTextInput}/>
    </div>
  )
}

ReactDOM.render(
  React.createElement(Chatroom, window.props),  // gets the props that are passed in the template
  window.react_mount,  // a reference to the div that we render to
)
