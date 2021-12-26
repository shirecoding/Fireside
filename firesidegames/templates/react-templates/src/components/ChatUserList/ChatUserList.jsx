import React from "react";
import { VariableSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const ROW_HEIGHT_WITH_HEADER = 36
const ROW_HEIGHT = 22

const renderRow = (props) => {
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
      <li className="list-group-item text-truncate border-0 py-0 my-0" style={style} key={index}>
        {data[index].uid}
      </li>
    );
  }
};

const ChatUserList = ({ users, friends, moderators }) => {
  /*
  Props:
    users: [{uid}]
    friends: [{uid}]
    moderators: [{uid}]
  */

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

  return (
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
            {renderRow}
          </VariableSizeList>
        )}
      </AutoSizer>
    </ul>
  );
};

export default ChatUserList;
