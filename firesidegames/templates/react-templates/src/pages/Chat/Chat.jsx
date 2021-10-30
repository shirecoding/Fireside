import ChatUserList from "../../components/ChatUserList";
import ChatTextField from "../../components/ChatTextField";
import ChatWindow from "../../components/ChatWindow";

const Chat = ({ messages, users, onTextInput }) => {

  return (
    <div className="row">
      <div className="col-9">
        <div className="row">
          <ChatWindow messages={messages} />
        </div>
        <div className="row">
          <ChatTextField onTextInput={onTextInput} />
        </div>
      </div>
      <div className="col-3">
        <ChatUserList users={users} />
      </div>
    </div>
  );
};

export default Chat;
