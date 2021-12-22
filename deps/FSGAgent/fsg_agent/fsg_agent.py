from agents import Agent, Message
from aiohttp import WSMsgType
from collections import defaultdict
import json

from .utils.message import FSGMessage, ChatMessage, User, Group, UpdateGroup, Method


class FSGAgent(Agent):
    def setup(self, host="0.0.0.0", port="8080", ws_route="/ws"):

        self.host = host
        self.port = port
        self.ws_route = ws_route

        # map connection to user and vice versa
        self.user_to_connection = {}
        self.connection_to_user = {}

        # map group to users
        self.groups = defaultdict(dict)

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

            # update connections table
            if isinstance(fsg_msg.sender, User):
                self.connection_to_user[msg.connection_id] = fsg_msg.sender.uid
                self.user_to_connection[fsg_msg.sender.uid] = msg.connection_id

            return fsg_msg
        return None

    def handle_update_group(self, message):
        """
        Update user groups

        TODO: There is a race condition if 2 message.users arrives and overwrites each other
        """

        # update table
        if message.method == Method.add:
            self.groups[message.receiver.uid].update({x.uid: x for x in message.users})
        else:
            self.groups[message.receiver.uid] = {x.uid: x for x in message.users}

        # update message
        message.method = Method.none
        message.users = list(self.groups[message.receiver.uid].values())

        # update all users in group
        for user_uid in self.groups[message.receiver.uid]:
            if user_uid in self.user_to_connection:
                message_out = Message.Websocket(
                    connection_id=self.user_to_connection[user_uid],
                    message=message.as_websocket(),
                    request=None,
                )
                self.log.debug(message_out)
                self.rtx.on_next(message_out)

    def handle_chat_message(self, message):
        """
        Relay message User or Group
        """

        receiver = message.receiver
        to_users = []

        if isinstance(receiver, User):
            to_users.append(receiver.uid)

        elif isinstance(receiver, Group) and receiver.uid in self.groups:
            to_users += self.groups[receiver.uid].keys()

        for user_uid in to_users:
            if user_uid in self.user_to_connection:
                message_out = Message.Websocket(
                    connection_id=self.user_to_connection[user_uid],
                    message=message.as_websocket(),
                    request=None,
                )
                self.log.debug(message_out)
                self.rtx.on_next(message_out)

    def handle_message(self, msg):

        message = self.parse_message(msg)

        # ChatMessage
        if isinstance(message, ChatMessage):
            self.handle_chat_message(message)

        # UpdateGroup
        elif isinstance(message, UpdateGroup):
            self.handle_update_group(message)
