import React from "react";
import Gameroom from "./Gameroom";
import _ from "lodash";

import { User, Group } from "../../fsg";

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
  benjamin: User({uid: "benjamin"}),
  matthew: User({uid: "matthew"}),
  mengxiong: User({uid: "mengxiong"}),
  alfathi: User({uid: "alfathi"}),
  winson: User({uid: "winson"}),
}

const group = Group({uid: "gameinstance_1"})

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
