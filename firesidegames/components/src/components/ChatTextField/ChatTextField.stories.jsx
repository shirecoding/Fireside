import React from "react";

import ChatTextField from "./ChatTextField";

export default {
  title: "Components/ChatTextField",
  component: ChatTextField,
  argTypes: {
    backgroundColor: { control: "color" },
  },
};

const Template = (args) => <ChatTextField {...args} />;

export const Primary = Template.bind({});
Primary.args = {};
