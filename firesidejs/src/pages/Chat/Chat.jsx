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
  paper: {
    height: 140,
    width: 100,
  },
  control: {
    padding: theme.spacing(2),
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
    <Grid container className={classes.root} spacing={2}>
      <Grid item xs={12}>
        <Grid container justifyContent="center" spacing={spacing}>
          <Grid item>
            <ChatWindow messages={messages} />
          </Grid>
          <Grid item>
            <UserList users={users} />
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <ChatTextField />
      </Grid>
    </Grid>
  );
};

export default Chat;
