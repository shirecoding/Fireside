const Method = {
  'add': 'add'
}

function User({uid}) {
  return {
    type: "User",
    uid: uid,
  }
}

function Group({uid}) {
  return {
    type: "Group",
    uid: uid,
  }
}

function ChatMessage({sender, receiver, message}) {
  return {
    type: "ChatMessage",
    sender: sender,
    receiver: receiver,
    message: message,
  }
}

function UpdateGroup({sender, receiver, users, method}) {
  return {
    type: "UpdateGroup",
    method: method,
    sender: sender,
    receiver: receiver,
    users: users,
  }
}

export {
  User,
  Group,
  ChatMessage,
  UpdateGroup,
  Method
};