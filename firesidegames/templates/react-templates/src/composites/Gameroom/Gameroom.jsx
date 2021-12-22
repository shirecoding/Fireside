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

  return (
    <Chat url={url} messages={messages} user={user} group={group} users={users} onTextInput={onTextInput}>
      <div className="d-flex align-content-start flex-wrap">
        {
          rooms.map(({uid}) => (
            <div className="card m-1" style={{width: "10rem", height: "10rem"}}>
              <div className="overflow-hidden position-relative border-radius-xl bg-cover">
                <span className="mask bg-gradient-dark"></span>
                <div className="card-body position-relative z-index-1 d-flex flex-column p-3">
                  <h5 className="text-white font-weight-bolder">{ uid }</h5>
                  <p className="text-white">{ uid }</p>
                  <a className="text-white text-sm font-weight-bold icon-move-right" href="javascript:;">
                    Go
                    <i className="fas fa-arrow-right text-sm ms-1"></i>
                  </a>
                </div>
              </div>
            </div>
          ))
        }
      </div>
    </Chat>
  )
};

export default Gameroom;
