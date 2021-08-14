import React, { useState, useEffect } from "react";
import { webSocket } from "rxjs/webSocket";

import Chat from "./pages/Chat";

const initialState = {
  messages: [
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
  ],
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};

const webSocketSubject = new webSocket("ws://127.0.0.1:8080/ws");

function App() {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    webSocketSubject.subscribe((e) => {
      setState((state) => {
        return { ...state, messages: [...state.messages, e] };
      });
    });
  }, []);

  return (
    <div>
      <Chat
        messages={state.messages}
        users={state.users}
        onTextInput={(e) => webSocketSubject.next(e)}
      />
    </div>
  );
}

export default App;
