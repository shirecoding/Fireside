import logo from "./logo.svg";
import "./App.css";

import Chat from "./pages/Chat";

const testData = {
  messages: [
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
  ],
  users: [{ name: "Luke Skywalker" }, { name: "Han Solo" }, { name: "Leia" }],
};

function App() {
  return (
    <div className="App">
      <Chat messages={testData.messages} users={testData.users} />
    </div>
  );
}

export default App;
