__all__ = ["Protocol"]

from abc import ABC
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    pass


class Protocol(BaseModel, ABC):
    protocol: str  # override accordingly (reserved keyword, use lowercase)
    klass: str  # import path if this class used for deserialization
