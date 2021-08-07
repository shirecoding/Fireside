import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "25ch",
    },
  },
}));

const ChatTextField = () => {
  const classes = useStyles();

  return <TextField id="outlined-basic" label="Chat" variant="outlined" />;
};

export default ChatTextField;
