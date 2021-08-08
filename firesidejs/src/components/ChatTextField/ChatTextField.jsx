import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
}));

const ChatTextField = () => {
  const classes = useStyles();

  return (
    <TextField
      id="outlined-basic"
      label="Chat"
      variant="outlined"
      className={classes.root}
    />
  );
};

export default ChatTextField;
