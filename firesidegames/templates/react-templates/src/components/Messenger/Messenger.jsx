import React, { useState } from "react";

import ChatWindow from "../ChatWindow";
import ChatTextField from "../ChatTextField";

const Messenger = ({contacts}) => {

  const [state, setState] = useState({showContacts: true, uid: null})

  if (state.showContacts) {
    return (
      <ul className="list-group h-100">{
        contacts.map(({uid}) => {
          return (
            <li className="d-flex align-items-end justify-content-between list-group-item text-truncate border-top-0 border-start-0 border-end-0 py-1 my-0"
            key={uid}
            onClick={() => setState({...state, showContacts: false, uid: uid})}>
              <div className="fw-bold">{uid}</div>
              <div><i className="fas fa-chevron-right"></i></div>
            </li>
          )
        })
      }</ul>
    )

  } else {
    return (
      <div className="card text-center rounded-0 border-0">
        <div className="card-header m-0 p-0 d-flex justify-content-between">
          <a className="align-self-center text-muted p-2" onClick={() => setState({...state, showContacts: true})}>
            <i className="fas fa-chevron-left me-1"></i>back
          </a>
          <div className="align-self-center flex-fill lead">
            {state.uid}
          </div>
        </div>
        <div className="card-body" style={{height: "200px"}}>
          <ChatWindow messages={[]}/>
        </div>
        <div className="card-footer text-muted m-0 p-0">
          <ChatTextField onTextInput={(x) => console.log(x)} />
        </div>
      </div>
    )
  }

};

export default Messenger;
