import React from 'react';
import ReactDOM from 'react-dom';
import Gameroom from "../composites/Gameroom";


const Root = ({user, users, group, messages, url, rooms}) => {

  return (
    <div className="container-fluid" style={{height: '500px'}}>
      <Gameroom user={user} users={users} group={group} messages={messages} url={url} rooms={rooms}/>
    </div>
  )
}

ReactDOM.render(
  React.createElement(Root, window.props),  // gets the props that are passed in the template
  window.react_mount,  // a reference to the div that we render to
)
