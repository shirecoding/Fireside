# Networking

- [verypowerfulagents](https://github.com/shirecoding/VeryPowerfulAgents)

# Architecture

## Processing & creating jobs

```
client1 -> agent1 -> process/create job -> redis
client2 -> agent1 -> process/create job -> redis
client3 -> agent2 -> process/create job -> redis
client4 -> agent2 -> process/create job -> redis
client5 -> agent2 -> process/create job -> redis
```

1. Clients send messages to agents via sockets

   - messages may include destination

2. Agents process the message

   - via a handler
   - may update world state
   - may create additional jobs

3. Agents place jobs in redis

## Consuming jobs

redis -> take job -> agent1 -> client1
redis -> take job -> agent1 -> client2
-> redis
redis -> take job -> agent2 -> client3
redis -> take job -> agent2 -> client4
-> redis
redis -> take job -> agent2 -> client5

1. Agents take jobs from redis

   - jobs may be specific to certain agents (depending on which clients they have a connection to)

2. Agents process job

   - may update world state

3. Agents send messages to clients

# Message payload

```json
// DirectMessage
{
    "type": "DirectMessage",
    "from": {
        "type": "User",
        "id": "benjamin",
        "session": "QWERTYUIO!@#$%^&"
    },
    "to": {
        "type": "User",
        "id": "mengxiong"
    },
    "message": "Hello world"
}

// ChatRoomMessage
{
    "type": "ChatRoomMessage",
    "from": {
        "type": "User",
        "id": "benjamin",
        "session": "QWERTYUIO!@#$%^&"
    },
    "to": {
        "type": "ChatRoom",
        "id": "room1"
    },
    "message": "Hello world"
}

// GlobalMessage
{
    "type": "GlobalMessage",
    "from": {
        "type": "User",
        "id": "benjamin",
        "session": "QWERTYUIO!@#$%^&"
    },
    "message": "Hello world"
}

// GameAction
{
    "type": "GameAction",
    "game": "firesideshooter1",
    "from": {
        "type": "User",
        "id": "benjamin",
        "session": "QWERTYUIO!@#$%^&"
    },
    "payload": {
        // game specific payload
    },
}
```

## Sessions

- middleware to check session of messages (add in verypowerfulagents)
- log users out if session is not valid
