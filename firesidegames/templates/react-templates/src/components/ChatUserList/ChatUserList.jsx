import React, { useState, useEffect } from "react";
import ReactDom from "react-dom"
import { VariableSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const ROW_HEIGHT_WITH_HEADER = 36
const ROW_HEIGHT = 22

const renderRow = (props, onClickUser) => {
  const { data, index, style } = props;

  if (data[index].type === "header") {
    return (
      <li className="d-flex align-items-end justify-content-between list-group-item text-truncate border-top-0 border-start-0 border-end-0 py-0 my-0" style={style} key={index}>
        <div className="fw-bold">{data[index].left}</div>
        <div>{data[index].right}</div>
      </li>
    );
  } else {
    return (
      <button className="list-group-item list-group-item-action text-truncate border-0 py-0 my-0"
      style={style} key={index} onClick={(e) => onClickUser(e, data[index].uid)}>
        {data[index].uid}
      </button>
    );
  }
};


const UserPopup = ({open, onClose, children}) => {

  const [el, setEl] = useState(document.createElement('div'))

  const handleClick = (e) => {
    if (open && !el.contains(e.target)) {
      onClose()
    }
  }

  useEffect(() => {
    document.body.appendChild(el);
    document.addEventListener("mousedown", handleClick);
    return () => {
      document.removeEventListener("mousedown", handleClick);
      document.body.removeChild(el);
    }
  }, [open])

  if (!open) {
    return null
  } else {
    return ReactDom.createPortal(children, el)
  }

}

const ChatUserList = ({ users, friends, moderators, onFriendRequest, onMail, onMessage}) => {
  /*
  Props:
    users: [{uid}]
    friends: [{uid}]
    moderators: [{uid}]
    onFriendRequest: Callback on friend request
    onMail: Callback on mail request
    onMessage: Callback on message request
  */

  const [state, setState] = useState({isUserPopupOpen: false, selectedUser: null, popupPos: [0, 0]})

  const headers = {
    "total": {"type": "header", "left": "TOTAL PLAYERS", "right": users.length},
    "moderators": {"type": "header", "left": "MODERATORS", "right": moderators.length},
    "friends": {"type": "header", "left": "FRIENDS", "right": friends.length},
    "lobby": {"type": "header", "left": "LOBBY", "right": users.length},
  }

  const rows = [headers.total, headers.moderators, ...moderators, headers.friends, ...friends, headers.lobby, ...users]

  const rowHeight = (index) => {
    return rows[index].type === "header" ? ROW_HEIGHT_WITH_HEADER : ROW_HEIGHT
  }

  const onClickUser = (e, uid) => {
    setState({...state, isUserPopupOpen: true, selectedUser: uid, popupPos: [e.clientX, e.clientY]})
  }

  const onSelect = (handler, ...args) => {
    handler(...args)
    setState({...state, isUserPopupOpen: false})
  }

  return (
    <div className="h-100">
      <ul className="list-group h-100">
        <AutoSizer>
          {({ height, width }) => (
            <VariableSizeList
              height={height}
              width={width}
              itemSize={rowHeight}
              itemCount={rows.length}
              itemData={rows}
            >
              {(props) => renderRow(props, onClickUser)}
            </VariableSizeList>
          )}
        </AutoSizer>
      </ul>
      <UserPopup open={state.isUserPopupOpen} onClose={() => setState({...state, isUserPopupOpen: false})}>
        <ul className="list-group" style={{width: "200px", position: "fixed", left: state.popupPos[0], top: state.popupPos[1]}}>
          <li className="list-group-item active py-1">{state.selectedUser}</li>
          <li className="list-group-item list-group-item-action py-1" onClick={() => onSelect(onMessage, state.selectedUser)}><i className="far fa-comment me-2"></i>Message</li>
          <li className="list-group-item list-group-item-action py-1" onClick={() => onSelect(onMail, state.selectedUser)}><i className="far fa-envelope me-2"></i>Mail</li>
          <li className="list-group-item list-group-item-action py-1" onClick={() => onSelect(onFriendRequest, state.selectedUser)}><i className="far fa-user me-2"></i>Friend Request</li>
        </ul>
      </UserPopup>
    </div>
  );
};

export default ChatUserList;
