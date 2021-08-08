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
  const { messages, users } = props;

  const [spacing, setSpacing] = React.useState(2);
  const classes = useStyles();

  const handleChange = (event) => {
    setSpacing(Number(event.target.value));
  };

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
          <ChatTextField />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Chat;
