import React from 'react';
import ReactDOM from 'react-dom';
import Gameroom from "../composites/Gameroom";
import { AppContext } from "../fsg";

const Root = ({user, users, group, messages, url, rooms, jwt, api}) => {

  return (
    <AppContext.Provider
      value={{
        user: user,
        jwt: jwt,
        url: url,
        api: api
      }}
    >
      <div className="container-fluid" style={{height: '500px'}}>
        <Gameroom users={users} group={group} messages={messages} rooms={rooms}/>
      </div>
    </AppContext.Provider>
  )
}

ReactDOM.render(
  React.createElement(Root, window.props),  // gets the props that are passed in the template
  window.react_mount,  // a reference to the div that we render to
)
