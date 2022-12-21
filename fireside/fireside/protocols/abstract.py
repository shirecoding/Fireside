__all__ = ["Protocol"]

from typing import TYPE_CHECKING, ClassVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from .defs import ProtocolDict


class Protocol(BaseModel):
    protocol: ClassVar[str]  # override accordingly (reserved keyword, use lowercase)

    def as_kwargs(self, jsonify: bool = False) -> "ProtocolDict":
        return {self.protocol: self.json() if jsonify else self}
