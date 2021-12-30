import React, { useContext } from "react";
import Chat from "../Chat";
import { ChatMessage, AppContext } from "../../fsg";

const Gameroom = ({ messages, group, users, rooms }) => {

  const { url, user, jwt, api } = useContext(AppContext)

  return (
    <Chat messages={messages} group={group} users={users}>
      <div className="d-flex align-content-start flex-wrap">
        {
          rooms.map(({uid}) => (
            <div className="card m-1 square-10-rem rounded-1 border-1" key={uid}>
              <div className="card-header fs-6 fw-bold text-truncate py-1 rounded-top text-white bg-primary">{ uid }</div>
              <div className="card-body d-flex align-items-center justify-content-center text-primary bg-transparent">
                <a className="btn btn-primary btn-circle" type="button">Join</a>
              </div>
            </div>
          ))
        }
      </div>
    </Chat>
  )
};

export default Gameroom;
