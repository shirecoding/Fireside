import React from "react";

import UserList from "./UserList";

export default {
  title: "Components/UserList",
  component: UserList,
};

const Template = (args) => (
  <div
    style={{
      height: "100vh",
      width: "100vw",
    }}
  >
    <UserList {...args} />;
  </div>
);

export const Primary = Template.bind({});
Primary.args = {
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};
