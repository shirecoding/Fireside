import React from "react";

import ChatUserList from "./ChatUserList";
import { User } from "../../fsg";

export default {
  title: "Components/ChatUserList",
  component: ChatUserList,
};

const users = [
  User({uid: "benjamin"}),
  User({uid: "matthew"}),
  User({uid: "mengxiong"}),
  User({uid: "alfathi"}),
  User({uid: "winson"}),
]

const Template = (args) => (
  <div
    style={{
      height: "100vh",
      width: "20vw",
    }}
  >
    <ChatUserList {...args} />;
  </div>
);

export const Primary = Template.bind({});
Primary.args = {
  users: users,
};
