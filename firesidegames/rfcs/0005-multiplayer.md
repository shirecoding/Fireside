# Multiplayer Concepts

## Game Client

- Inform other clients and game master (a special client) of it's events
- Simulate received events in the game engine and how it affects the player
- Events contains the sender and event properties

## Game Master

- Serverless Godot
- Runs a copy of the game client
- Always need 1 per game instance
- Inform other players of it's events (world events)
- Simulate received events and how it affects the world (itself)
- World events
    - Game start/end
    - Things getting destroyed
- Mantains data of the game state
    - kill/deaths
    - score
