import React, { useState } from "react";
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
      style={style} key={index} onClick={() => onClickUser(data[index].uid)}>
        {data[index].uid}
      </button>
    );
  }
};


class UserPopup extends React.Component {

  constructor(props) {
    super(props);
    this.el = document.createElement('div');
  }

  componentDidMount() {
    document.body.appendChild(this.el);
  }

  componentWillUnmount() {
    document.body.removeChild(this.el);
  }

  render() {
    if (!this.props.open) {
      return null
    } else {
      return ReactDom.createPortal(this.props.children, this.el)
    }
  }

}


const ChatUserList = ({ users, friends, moderators }) => {
  /*
  Props:
    users: [{uid}]
    friends: [{uid}]
    moderators: [{uid}]
  */

  const [state, setState] = useState({isUserPopupOpen: false, selectedUser: null})

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

  const onClickUser = (uid) => {
    setState({...state, isUserPopupOpen: true, selectedUser: uid})
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
        <ul className="list-group">
          <li className="list-group-item active">{state.selectedUser}</li>
          <li className="list-group-item list-group-item-action"><i className="far fa-comment me-2"></i>Message</li>
          <li className="list-group-item list-group-item-action"><i className="far fa-envelope me-2"></i>Mail</li>
          <li className="list-group-item list-group-item-action"><i className="far fa-user me-2"></i>Friend Request</li>
        </ul>
      </UserPopup>
    </div>
  );
};

export default ChatUserList;
