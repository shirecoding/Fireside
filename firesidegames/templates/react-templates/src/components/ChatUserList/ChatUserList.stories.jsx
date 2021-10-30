import React from "react";

import ChatUserList from "./ChatUserList";

export default {
  title: "Components/ChatUserList",
  component: ChatUserList,
};

const Template = (args) => (
  <div className="container-fluid h-100 w-50">
    <ChatUserList {...args} />;
  </div>
);

export const Primary = Template.bind({});
Primary.args = {
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};
