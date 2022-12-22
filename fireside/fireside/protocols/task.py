__all = ["PTaskChain"]

from fireside.protocols import Protocol

from .defs import TaskTree


class PTaskChain(Protocol):
    protocol: str = "ptaskchain"
    task_chain: list[TaskTree]
