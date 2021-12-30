import React from "react";
import Gameroom from "./Gameroom";
import _ from "lodash";

import { User, Group, AppContext } from "../../fsg";

export default {
  title: "Composites/Gameroom",
  component: Gameroom,
};

const Template = (args) => (
  <AppContext.Provider
    value={{
      user: args.user,
      jwt: args.jwt,
      url: args.url,
      api: args.api,
    }}
  >
    <div className="container-fluid" style={{height: '500px'}}>
      <Gameroom {...args}/>
    </div>
  </AppContext.Provider>
)

export const Primary = Template.bind({});

const users = {
  benjamin: User({uid: "benjamin"}),
  matthew: User({uid: "matthew"}),
  mengxiong: User({uid: "mengxiong"}),
  alfathi: User({uid: "alfathi"}),
  winson: User({uid: "winson"}),
}

const group = Group({uid: "gamelobby_1"})

const rooms = [
  {uid: "gameinstance_1"},
  {uid: "gameinstance_2"},
  {uid: "gameinstance_3"},
  {uid: "gameinstance_4"},
  {uid: "gameinstance_5"},
  {uid: "gameinstance_6"},
  {uid: "gameinstance_7"},
  {uid: "gameinstance_8"},
  {uid: "gameinstance_9"},
  {uid: "gameinstance_10"},
  {uid: "gameinstance_11"},
]

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
  rooms: rooms,
  user: users.benjamin,
  group: group,
  users: _.values(users),
};
