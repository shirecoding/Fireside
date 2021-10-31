import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";
import Chat from "./Chat";

export default {
  title: "Pages/Chat",
  component: Chat,
};

const webSocketSubject = new webSocket("ws://127.0.0.1:8080/ws");

// close websocket on browser unload
window.onbeforeunload = () => {
  console.log("closing websocket ...");
  webSocketSubject.complete();
};

const Template = (args) => (
  <div className="container-fluid" >
    <Chat {...args} />
  </div>
)

export const Primary = Template.bind({});

Primary.args = {
  messages: [
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "benjamin hon weng kiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "matthew"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "meng xiong"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "jansen"},
    {message: "The quick brown fox jumps over the lazy dog.", user: "eugene"},
  ],
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};
