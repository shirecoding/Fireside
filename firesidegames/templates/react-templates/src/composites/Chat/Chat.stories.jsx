import React from "react";
import Chat from "./Chat";
import {ChatMessage, User, Group} from "../../fsg";
import _ from "lodash";

export default {
  title: "Composites/Chat",
  component: Chat,
};

const Template = (args) => (
  <div className="container-fluid" style={{height: '500px'}}>
    <Chat {...args}/>
  </div>
)

export const Primary = Template.bind({});

const users = {
  benjamin: User({uid: "benjamin"}),
  matthew: User({uid: "matthew"}),
  mengxiong: User({uid: "mengxiong"}),
  alfathi: User({uid: "alfathi"}),
  winson: User({uid: "winson"}),
}


const group = Group({uid: "gameinstance_1"})

const onTextInput = (state, e) => {
  if (state.webSocket) {
    state.webSocket.next(ChatMessage({
      sender: users.benjamin,
      receiver: group,
      message: e,
    }))
  }
}

Primary.args = {
  url: "ws://127.0.0.1:8080/ws",
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
  ],
  user: users.benjamin,
  group: group,
  users: _.values(users),
  onTextInput: onTextInput,
  onFriendRequest: (uid) => console.log(`onFriendRequest ${uid}`),
  onMessage: (uid) => console.log(`onMessage ${uid}`),
  onMail: (uid) => console.log(`onMail ${uid}`)
};
