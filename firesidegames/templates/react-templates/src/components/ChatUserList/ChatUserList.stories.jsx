import React from "react";

import ChatUserList from "./ChatUserList";
import { User } from "../../fsg";

export default {
  title: "Components/ChatUserList",
  component: ChatUserList,
};

const users = [
  new User({uid: "benjamin"}),
  new User({uid: "matthew"}),
  new User({uid: "mengxiong"}),
  new User({uid: "alfathi"}),
  new User({uid: "winson"}),
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
