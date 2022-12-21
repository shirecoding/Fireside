__all__ = ["ProtocolDict"]

from typing import Union

from fireside.utils import JSONObject

from .abstract import Protocol

ProtocolDict = dict[str, Union[Protocol, JSONObject]]
