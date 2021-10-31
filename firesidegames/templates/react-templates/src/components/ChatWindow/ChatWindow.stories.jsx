import React from "react";

import ChatWindow from "./ChatWindow";

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

export const Primary = Template.bind({});
Primary.args = {
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
  ],
};
