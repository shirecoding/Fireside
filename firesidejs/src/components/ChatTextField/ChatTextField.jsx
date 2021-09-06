import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
}));

const ChatTextField = (props) => {
  const classes = useStyles();
  const { onTextInput } = props;

  return (
    <TextField
      id="outlined-basic"
      label="Chat"
      variant="outlined"
      size="small"
      className={classes.root}
      onKeyDown={(e) => {
        if (e.keyCode === 13) {
          onTextInput(e.target.value);
          e.target.value = "";
        }
      }}
    />
  );
};

export default ChatTextField;
