import React from 'react';
import ReactDOM from 'react-dom';
import {GlobalMessage, User} from "../fsg";
import Chat from "../composites/Chat";


const Chatroom = ({users, messages, url}) => {

  const onTextInput = (state, e) => {
    if (state.webSocket) {
      const sender = new User({id: "benjamin", session: "QWERTYUIO!@#$%^&"})
      const msg = new GlobalMessage({message: e, sender: sender})
      state.webSocket.next(msg)
    }
  }

  return (
    <div className="container-fluid" style={{height: '500px'}}>
      <Chat users={users} messages={messages} url={url} onTextInput={onTextInput}/>
    </div>
  )
}

ReactDOM.render(
  React.createElement(Chatroom, window.props),  // gets the props that are passed in the template
  window.react_mount,  // a reference to the div that we render to
)
