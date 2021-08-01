import React from 'react';

import ChatTextField from '../components/ChatTextField';

export default {
  title: 'Fireside/ChatTextField',
  component: ChatTextField,
  argTypes: {
    backgroundColor: { control: 'color' },
  },
};

const Template = (args) => <ChatTextField {...args} />;

export const Primary = Template.bind({});
Primary.args = {
};
