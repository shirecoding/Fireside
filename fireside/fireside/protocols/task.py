__all = ["PTaskChain", "PProtocolDict"]

from pydantic import validator

from .abstract import Protocol
from .defs import ProtocolDict, TaskTree
from .utils import as_deserialized_pdict


class PTaskChain(Protocol):
    protocol: str = "ptaskchain"
    klass: str = "fireside.protocols.task.PTaskChain"
    task_chain: list[TaskTree]


class PProtocolDict(Protocol):
    protocol: str = "pprotocoldict"
    klass: str = "fireside.protocols.task.PProtocolDict"
    protocols: ProtocolDict

    @validator("protocols", pre=True)
    def ensure_serialized(cls, pdict):
        # serialize the generic instances into their specific klass
        return as_deserialized_pdict(pdict)
