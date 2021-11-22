import React from "react";
import Gameroom from "./Gameroom";
import _ from "lodash";

import { GlobalMessage, User, Group } from "../../fsg";

export default {
  title: "Composites/Gameroom",
  component: Gameroom,
};

const Template = (args) => (
  <div className="container-fluid" style={{height: '500px'}}>
    <Gameroom {...args}/>
  </div>
)

export const Primary = Template.bind({});

const users = {
  benjamin: new User({uid: "benjamin"}),
  matthew: new User({uid: "matthew"}),
  mengxiong: new User({uid: "mengxiong"}),
  alfathi: new User({uid: "alfathi"}),
  winson: new User({uid: "winson"}),
}

const group = new Group({uid: "gameinstance_1"})

Primary.args = {
  url: "ws://127.0.0.1:8080/ws",
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.benjamin},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.matthew},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.mengxiong},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.alfathi},
    {message: "The quick brown fox jumps over the lazy dog.", user: users.winson},
  ],
  user: users.benjamin,
  group: group,
  users: _.values(users),
};
