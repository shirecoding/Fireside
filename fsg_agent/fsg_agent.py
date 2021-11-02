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
        )  # Note: connections is read only, do not modify
        self.disposables.append(self.rtx.subscribe(self.handle_message))

    def parse_message(self, msg):
        if msg.message.type in [WSMsgType.TEXT, WSMsgType.BINARY]:
            return FSGMessage.parse(json.parse(msg.message.data))
        return None

    def handle_global_message(self, message):
        """
        Broadcast message to all connections
        """
        for _id in self.connections.keys():
            if _id in self.connection_to_user:
                message_out = Message.Websocket(
                    connection_id=_id,
                    message=DirectMessage(
                        message=message.message,
                        receiver=User(id=self.connection_to_user[_id]),
                    ).as_websocket(),
                    request=None,
                )
                self.log.debug(message_out)
                self.rtx.on_next(message_out)
            else:
                self.log.debug(f"connection {_id} cannot be mapped to a user ...")

    def handle_message(self, msg):

        message = self.parse_message(msg)

        # GlobalMessage
        if isinstance(message, GlobalMessage):
            self.handle_global_message(message)
