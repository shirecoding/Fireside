from agents import Agent, Message
from aiohttp import WSMsgType
import json

from .utils.message import FSGMessage, GlobalMessage, DirectMessage, User


class FSGAgent(Agent):
    def setup(self, host="0.0.0.0", port="8080", ws_route="/ws"):

        self.host = host
        self.port = port
        self.ws_route = ws_route

        # map connection to user and vice versa
        self.user_to_connection = {}
        self.connection_to_user = {}

        # create webserver - required for websocket
        self.create_webserver(host, int(port))

        # create websocket and subscribe
        self.rtx, self.connections = self.create_websocket(
            ws_route
        )  # Note: connections map connection_id to websockets it is read only, do not modify
        self.disposables.append(self.rtx.subscribe(self.handle_message))

    def parse_message(self, msg):
        if msg.message.type in [WSMsgType.TEXT, WSMsgType.BINARY]:
            fsg_msg = FSGMessage.parse(json.loads(msg.message.data))
            # update connections
            if hasattr(fsg_msg, "sender") and isinstance(fsg_msg.sender, User):
                self.connection_to_user[msg.connection_id] = fsg_msg.sender.id
                self.user_to_connection[fsg_msg.sender.id] = msg.connection_id
            return fsg_msg
        return None

    def handle_global_message(self, message):
        """
        Broadcast message to all connections
        """
        for connection_id, user_id in self.connection_to_user.items():
            message_out = Message.Websocket(
                connection_id=connection_id,
                message=DirectMessage(
                    message=message.message,
                    receiver=User(id=user_id),
                ).as_websocket(),
                request=None,
            )
            self.log.debug(message_out)
            self.rtx.on_next(message_out)

    def handle_message(self, msg):

        message = self.parse_message(msg)

        # GlobalMessage
        if isinstance(message, GlobalMessage):
            self.handle_global_message(message)
