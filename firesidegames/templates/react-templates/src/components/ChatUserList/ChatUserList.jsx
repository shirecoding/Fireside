import React from "react";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <li className="list-group-item text-truncate border-0" style={style} key={index}>
      {data[index].name}
    </li>
  );
};

const ChatUserList = ({ users }) => {

  return (
    <ul className="list-group h-100">
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            height={height}
            width={width}
            itemSize={42}
            itemCount={users.length}
            itemData={users}
          >
            {renderRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </ul>
  );
};

export default ChatUserList;
