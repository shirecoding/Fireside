import React, { useCallback, useEffect } from "react";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <li className="list-group-item fs-6" style={style} key={index}>
      {data[index]}
    </li>
  );
};

const ChatWindow = ({ messages }) => {

  const fixedSizeListRef = useCallback((node) => {
    if (node !== null) {
      node.scrollToItem(messages.length - 1, "end");
    }
  });

  return (
    <ul className="list-group list-group-flush vh-100">
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            ref={fixedSizeListRef}
            height={height}
            width={width}
            itemSize={42}
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
