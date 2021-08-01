import React from 'react';

import UserList from '../components/UserList';

export default {
  title: 'Fireside/UserList',
  component: UserList,
};

const Template = (args) => <UserList {...args} />;

export const Primary = Template.bind({});
Primary.args = {};