class User {
  constructor({uid}) {
    this.type = "User"
    this.uid = uid
  }
}

class Group {
  constructor({uid}) {
    this.type = "Group"
    this.uid = uid
  }
}

class ChatMessage {
  constructor({sender, receiver, message}) {
    this.type = "ChatMessage"
    this.sender = sender
    this.receiver = receiver
    this.message = message
  }
}

class UpdateGroup {
  constructor({sender, receiver, users}) {
    this.type = "UpdateGroup"
    this.sender = sender
    this.receiver = receiver
    this.users = users
  }
}

export {
  User,
  Group,
  ChatMessage,
  UpdateGroup
};