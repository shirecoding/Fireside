import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

import UserList from "../../components/UserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
}));

const Chat = (props) => {
  const classes = useStyles();
  const { messages, users, onTextInput } = props;

  return (
    <Grid container className={classes.root} spacing={1}>
      <Grid item xs={2}>
        <UserList users={users} />
      </Grid>
      <Grid container item xs={10} spacing={1} direction="column">
        <Grid item xs>
          <ChatWindow messages={messages} />
        </Grid>
        <Grid item xs>
          <ChatTextField onTextInput={onTextInput} />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Chat;
