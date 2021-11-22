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
  benjamin: new User({uid: "benjamin"}),
  matthew: new User({uid: "matthew"}),
  mengxiong: new User({uid: "mengxiong"}),
  alfathi: new User({uid: "alfathi"}),
  winson: new User({uid: "winson"}),
}

const group = new Group({uid: "gameinstance_1"})

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
  onTextInput: (state, e) => {
    if (state.webSocket) {
      state.webSocket.next(new ChatMessage({
        sender: users.benjamin,
        receiver: group,
        message: e,
      }))
    }
  }
};
