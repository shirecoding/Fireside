__all__ = ["Protocol"]

from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .defs import ProtocolDict


class Protocol(BaseModel, ABC):
    protocol: str  # override accordingly (reserved keyword, use lowercase)
    klass: str  # import path if this class used for deserialization

    def as_pdict(self, jsonify: bool = False) -> "ProtocolDict":
        return {self.protocol: self.dict() if jsonify else self}
