__all__ = ["User", "DirectMessage", "GlobalMessage", "FSGMessage", "Method"]

from dataclasses import dataclass, asdict, field
from aiohttp import WSMessage, WSMsgType
import json
from typing import Union


@dataclass
class BaseType:
    type: str = "BaseType"


class MessageMixin:
    def as_websocket(self):
        return WSMessage(type=WSMsgType.TEXT, data=json.dumps(asdict(self)), extra=None)

    def as_dict(self):
        return asdict(self)


@dataclass
class User(BaseType):
    type: str = "User"
    uid: str = None


@dataclass
class Group(BaseType):
    type: str = "Group"
    uid: str = None


class Method:
    none = ""
    add = "add"


@dataclass
class BaseMessage(MessageMixin):
    type: str = "BaseMessage"
    sender: Union[User, Group] = None
    receiver: Union[User, Group] = None


@dataclass
class ChatMessage(BaseMessage):
    """
    {
        "type": "ChatMessage",
        "sender": {
            "type": "User",
            "uid": "benjamin",
        },
        "receiver": {
            "type": "Group",
            "uid": "gameroom1"
        },
        "message": "Hello world"
    }
    """

    type: str = "ChatMessage"
    message: str = None


@dataclass
class UpdateGroup(BaseMessage):
    """
    {
        "type": "UpdateGroup",
        "sender": {
            "type": "User",
            "uid": "benjamin",
        },
        "receiver": {
            "type": "Group",
            "uid": "gameroom1",
        },
        "method": "add",
        "users": ['benjamin', 'mengxiong']
    }
    """

    type: str = "UpdateGroup"
    users: list[str] = field(default_factory=list)
    method: str = ""


class FSGMessage:

    lookup = {
        "UpdateGroup": UpdateGroup,
        "ChatMessage": ChatMessage,
        "BaseMessage": BaseMessage,
        "User": User,
        "Group": Group,
    }

    @classmethod
    def parse(cls, message):
        return cls.lookup[message["type"]](
            **{
                k: cls.parse(v)
                if isinstance(v, dict)
                else [cls.parse(x) for x in v]
                if isinstance(v, list)
                else v
                for k, v in message.items()
            }
        )
