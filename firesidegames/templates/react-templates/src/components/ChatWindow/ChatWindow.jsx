import React, { useCallback } from "react";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <li className="list-group-item border-0" style={style} key={index}>
      <div className="ms-2 me-auto">
        <div className="fw-bold">{data[index].user.uid}</div>
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
            itemSize={64}
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
