__all = ["PTaskChain"]

from fireside.protocols import Protocol

from .defs import TaskTree


class PTaskChain(Protocol):
    protocol: str = "ptaskchain"
    klass: str = "fireside.protocols.task.PTaskChain"
    task_chain: list[TaskTree]
