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
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
  ],
};
