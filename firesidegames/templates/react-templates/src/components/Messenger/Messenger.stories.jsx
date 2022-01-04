import React from "react";

import Messenger from "./Messenger";
import { action } from '@storybook/addon-actions';
import { User } from "../../fsg";

export default {
  title: "Components/Messenger",
  component: Messenger,
  argTypes: {
    backgroundColor: { control: "color" },
  },
};

const Template = (args) => (
  <div
    style={{
      height: "100vh",
      width: "40vw",
    }}
  >
    <Messenger {...args} />
  </div>
)

const users = [
  User({uid: "benjamin"}),
  User({uid: "matthew"}),
  User({uid: "mengxiong"}),
  User({uid: "alfathi"}),
  User({uid: "winson"}),
]


export const Primary = Template.bind({});

Primary.args = {
  contacts: users
};
