import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { FixedSizeList } from "react-window";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    height: 400,
    maxWidth: 300,
    backgroundColor: theme.palette.background.paper,
  },
}));

const renderRow = (props) => {
  const { data, index, style } = props;
  return (
    <ListItem button style={style} key={index}>
      <ListItemText primary={data[index]} />
    </ListItem>
  );
};

const ChatWindow = ({ messages }) => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <FixedSizeList
        height={400}
        width={600}
        itemSize={46}
        itemCount={messages.length}
        itemData={messages}
      >
        {renderRow}
      </FixedSizeList>
    </div>
  );
};

export default ChatWindow;
