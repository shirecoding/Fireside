__all__ = ["Protocol", "ProtocolDict", "JSONObject"]

from typing import Any, ClassVar, Union

from pydantic import BaseModel

JSONObject = dict[str, Any]

ProtocolDict = dict[str, Union["Protocol", JSONObject]]


class Protocol(BaseModel):
    protocol: ClassVar[str]  # override accordingly (reserved keyword, use lowercase)

    def as_kwargs(self, jsonify: bool = False) -> ProtocolDict:
        return {self.protocol: self.json() if jsonify else self}
