import React, { useState } from "react";

const ChatTextField = ({onTextInput, selections=['Chat']}) => {

  const [selection, setSelection] = useState(selections[0]);

  return (
    <div className="input-group d-flex">
      <button className="btn btn-outline-secondary dropdown-toggle py-0" type="button" data-bs-toggle="dropdown" aria-expanded="false">{selection}</button>
      <ul className="dropdown-menu">{
        selections.map((x) => <li key={x}><a className="dropdown-item" onClick={(v) => setSelection(v.target.text)}>{x}</a></li>)
      }</ul>
      <div className="mb-3 flex-fill py-0">
        <input type="text" className="form-control chat-input" placeholder="..." onKeyDown={(e) => {
          if (e.keyCode === 13) {
            onTextInput(e.target.value);
            e.target.value = "";
          }
        }}/>
      </div>
    </div>
  );
};

export default ChatTextField;
