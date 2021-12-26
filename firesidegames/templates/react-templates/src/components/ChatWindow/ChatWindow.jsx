import React, { useCallback } from "react";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <li className="d-flex align-items-end list-group-item border-0 p-0 m-0" style={style} key={index}>
      <div className="fw-bold text-right me-3 ms-0 text-truncate" style={{width: "8rem"}}>
        {data[index].user.uid}
      </div>
      <div className="text-left text-truncate" style={{width: "42rem"}}>
        {data[index].message}
      </div>
    </li>
  );
};

const ChatWindow = ({ messages }) => {

  const fixedSizeListRef = useCallback((node) => {
    if (node !== null) {
      node.scrollToItem(messages.length - 1, "end");
    }
  }, [messages]);

  return (
    <ul className="list-group h-100">
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            ref={fixedSizeListRef}
            height={height}
            width={width}
            itemSize={26}
            itemCount={messages.length}
            itemData={messages}
          >
            {renderRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </ul>
  );
};

export default ChatWindow;
