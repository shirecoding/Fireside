import React from "react";

import ChatWindow from "./ChatWindow";

import { User } from "../../fsg";

export default {
  title: "Components/ChatWindow",
  component: ChatWindow,
};

const Template = (args) => (
  <div
    style={{
      height: "100vh",
      width: "70vw",
    }}
  >
    <ChatWindow {...args} />;
  </div>
);

const users = {
  benjamin: User({uid: "benjamin"}),
  matthew: User({uid: "matthew"}),
  mengxiong: User({uid: "mengxiong"}),
  alfathi: User({uid: "alfathi"}),
  winson: User({uid: "winson"}),
}

export const Primary = Template.bind({});
Primary.args = {
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
  ],
};
