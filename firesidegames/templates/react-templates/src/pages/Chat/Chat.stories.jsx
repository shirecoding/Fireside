import React from "react";
import Chat from "./Chat";

export default {
  title: "Pages/Chat",
  component: Chat,
};

const Template = (args) => (
  <div className="container-fluid" >
    <Chat {...args} />
  </div>
)

export const Primary = Template.bind({});
Primary.args = {
  messages: [
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
  ],
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};
