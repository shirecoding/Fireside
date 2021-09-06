import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

import UserList from "../../components/UserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    height: "100vh",
    width: "100%",
  },
}));

const Chat = ({ messages, users, onTextInput }) => {
  const classes = useStyles();

  return (
    <Grid container className={classes.root} spacing={1} direction="row">
      <Grid
        container
        item
        xs={10}
        spacing={1}
        direction="column"
        justifyContent="flex-end"
      >
        <Grid item>
          <ChatWindow messages={messages} />
        </Grid>
        <Grid item>
          <ChatTextField onTextInput={onTextInput} />
        </Grid>
      </Grid>
      <Grid item xs={2}>
        <UserList users={users} />
      </Grid>
    </Grid>
  );
};

export default Chat;
