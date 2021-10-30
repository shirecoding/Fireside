import React from "react";

const ChatTextField = (props) => {

  const { onTextInput } = props;

  return (
    <div className="input-group">
      <input type="text" className="form-control" aria-label="Text input with segmented dropdown button"/>
      <button type="button" className="btn btn-outline-secondary">Action</button>
      <button type="button" className="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
        <span className="visually-hidden">Toggle Dropdown</span>
      </button>
      <ul className="dropdown-menu dropdown-menu-end">
        <li><a className="dropdown-item" href="#">Action</a></li>
        <li><a className="dropdown-item" href="#">Another action</a></li>
        <li><a className="dropdown-item" href="#">Something else here</a></li>
        <li><hr className="dropdown-divider"/></li>
        <li><a className="dropdown-item" href="#">Separated link</a></li>
      </ul>
    </div>
  );
};

export default ChatTextField;
