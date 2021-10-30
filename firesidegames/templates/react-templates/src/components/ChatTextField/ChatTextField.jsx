import React from "react";

const ChatTextField = (props) => {

  const { onTextInput } = props;

  return (
    <div className="input-group">
      <button className="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Dropdown</button>
      <ul className="dropdown-menu">
        <li><a className="dropdown-item" href="#">Action</a></li>
        <li><a className="dropdown-item" href="#">Another action</a></li>
        <li><a className="dropdown-item" href="#">Something else here</a></li>
        <li><hr className="dropdown-divider"/></li>
        <li><a className="dropdown-item" href="#">Separated link</a></li>
      </ul>
      <input type="text" className="form-control" placeholder="..." onKeyDown={(e) => {
        if (e.keyCode === 13) {
          onTextInput(e.target.value);
          e.target.value = "";
        }
      }}/>
    </div>
  );
};

export default ChatTextField;
