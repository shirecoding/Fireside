import React from "react";
import Chat from "../Chat";
import { ChatMessage } from "../../fsg";

const Gameroom = ({ url, messages, user, group, users, rooms, jwt }) => {

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

  const onFriendRequest = (uid) => {
    console.log(`onFriendRequest: ${uid}`)
  }

  const onMail = (uid) => {
    console.log(`onMail: ${uid}`)
  }

  const onMessage = (uid) => {
    console.log(`onMessage: ${uid}`)
  }

  return (
    <Chat url={url} messages={messages} user={user} group={group} users={users} jwt={jwt}
    onTextInput={onTextInput} onFriendRequest={onFriendRequest} onMail={onMail} onMessage={onMessage}>
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
