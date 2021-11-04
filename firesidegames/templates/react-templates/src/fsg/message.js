class User {
  constructor({id, session}) {
    this.type = "User"
    this.id = id
    this.session = session
  }
}

class GlobalMessage {
  constructor({sender, message}) {
    this.type = "GlobalMessage"
    this.sender = sender
    this.message = message
  }
}

class DirectMessage {
  constructor({sender, receiver, message}) {
    this.type = "DirectMessage"
    this.sender = sender
    this.receiver = receiver
    this.message = message
  }
}

export {
  User,
  GlobalMessage,
  DirectMessage
};