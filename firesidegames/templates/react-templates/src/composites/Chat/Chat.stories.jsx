import React from "react";
import Chat from "./Chat";

import {GlobalMessage, User} from "../../fsg";

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

Primary.args = {
  url: "ws://127.0.0.1:8080/ws",
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
  ],
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
  onTextInput: (state, e) => {
    if (state.webSocket) {
      const sender = new User({id: "benjamin", session: "QWERTYUIO!@#$%^&"})
      const msg = new GlobalMessage({message: e, sender: sender})
      state.webSocket.next(msg)
    }
  }
};
