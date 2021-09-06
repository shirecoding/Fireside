import React, { useCallback, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { FixedSizeList } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    height: 110,
    backgroundColor: theme.palette.background.paper,
  },
  row: {
    fontSize: "small",
  },
}));

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <ListItem button style={style} key={index}>
      <ListItemText secondary={data[index]} />
    </ListItem>
  );
};

const ChatWindow = ({ messages }) => {
  const classes = useStyles();

  const fixedSizeListRef = useCallback((node) => {
    if (node !== null) {
      node.scrollToItem(messages.length - 1, "end");
    }
  });

  return (
    <div className={classes.root}>
      <AutoSizer>
        {({ height, width }) => (
          <FixedSizeList
            ref={fixedSizeListRef}
            height={height}
            width={width}
            itemSize={20}
            itemCount={messages.length}
            itemData={messages}
          >
            {renderRow}
          </FixedSizeList>
        )}
      </AutoSizer>
    </div>
  );
};

export default ChatWindow;
