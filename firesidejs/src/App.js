import React, { useState, useEffect } from "react";
import { Subject } from "rxjs";

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

const subject = new Subject();
const textEmitter = new Subject();

function App() {
  const [state, setState] = useState(initialState);

  useEffect(() => {
    subject.subscribe(setState);
    textEmitter.subscribe((e) => {
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
        onTextInput={(e) => textEmitter.next(e)}
      />
    </div>
  );
}

export default App;
