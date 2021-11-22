import React, { useState } from "react";
import Chat from "../Chat";
import _ from "lodash";
import { ChatMessage } from "../../fsg";

const Gameroom = ({ url, messages, user, group, users, rooms }) => {

  const onTextInput = (chatState, e) => {
    if (chatState.webSocket) {
      chatState.webSocket.next(
        ChatMessage({
          message: e,
          sender: user,
          receiver: group
        })
      )
    }
  }

  const roomsPerPage = 3;

  const [state, setState] = useState({
    page: 0,
  });

  return (
    <Chat url={url} messages={messages} user={user} group={group} users={users} onTextInput={onTextInput}>
      <div className="row">
        {
          rooms.slice(state.page * roomsPerPage, state.page * roomsPerPage + roomsPerPage).map(({uid}) => (
            <div className="col-4">
              <div className="card mb-4">
                <div className="overflow-hidden position-relative border-radius-xl bg-cover h-100">
                  <span className="mask bg-gradient-dark"></span>
                  <div className="card-body position-relative z-index-1 d-flex flex-column h-100 p-3">
                    <h5 className="text-white font-weight-bolder mb-4 pt-2">{ uid }</h5>
                    <p className="text-white">{ uid }</p>
                    <a className="text-white text-sm font-weight-bold mb-0 icon-move-right mt-auto" href="javascript:;">
                      Go
                      <i className="fas fa-arrow-right text-sm ms-1"></i>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          ))
        }
      </div>
      <nav className="d-flex justify-content-center">
        <ul className="pagination pagination-sm">
          {
            _.range(Math.ceil(rooms.length / roomsPerPage)).map((i) => (
              <li className={state.page == i ? "page-item active" : "page-item"}>
                <a className="page-link"
                  onClick={(e) => {
                    e.preventDefault();
                    setState({...state, page: i});
                  }}
                >
                  {i}
                </a>
              </li>
            ))
          }
        </ul>
      </nav>
    </Chat>
  )
};

export default Gameroom;
