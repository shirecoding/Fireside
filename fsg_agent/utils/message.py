__all__ = ["User", "DirectMessage", "GlobalMessage", "FSGMessage"]

from dataclasses import dataclass, asdict
from aiohttp import WSMessage, WSMsgType
import json


class MessageMixin:
    def as_websocket(self):
        return WSMessage(type=WSMsgType.TEXT, data=json.dumps(asdict(self)), extra=None)

    def as_dict(self):
        return asdict(self)


@dataclass
class User:
    type: str = "User"
    id: str = None
    session: str = None


@dataclass
class DirectMessage(MessageMixin):
    """
    {
        "type": "DirectMessage",
        "sender": {
            "type": "User",
            "id": "benjamin",
            "session": "QWERTYUIO!@#$%^&"
        },
        "receiver": {
            "type": "User",
            "id": "mengxiong"
        },
        "message": "Hello world"
    }
    """

    type: str = "DirectMessage"
    message: str = None
    receiver: User = None
    sender: User = None


@dataclass
class GlobalMessage(MessageMixin):
    """
    {
        "type": "GlobalMessage",
        "sender": {
            "type": "User",
            "id": "benjamin",
            "session": "QWERTYUIO!@#$%^&"
        },
        "message": "Hello world"
    }
    """

    type: str = "GlobalMessage"
    message: str = None
    sender: User = None


class FSGMessage:

    lookup = {
        "DirectMessage": DirectMessage,
        "GlobalMessage": GlobalMessage,
        "User": User,
    }

    @classmethod
    def parse(cls, message):
        return cls.lookup[message["type"]](
            **{
                k: cls.parse(v) if isinstance(v, dict) else v
                for k, v in message.items()
            }
        )
