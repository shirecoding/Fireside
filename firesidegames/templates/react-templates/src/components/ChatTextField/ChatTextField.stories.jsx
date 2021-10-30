import React from "react";

import ChatTextField from "./ChatTextField";
import { action } from '@storybook/addon-actions';

export default {
  title: "Components/ChatTextField",
  component: ChatTextField,
  argTypes: {
    backgroundColor: { control: "color" },
  },
};

const Template = (args) => <ChatTextField {...args} onTextInput={action('onTextInput')} />;

export const Primary = Template.bind({});

Primary.args = {};
