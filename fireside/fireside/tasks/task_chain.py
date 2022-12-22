__all = ["task_chain"]

import logging

from fireside.protocols import Protocol, PTaskChain
from fireside.utils.task import task

logger = logging.getLogger(__name__)


@task(name="TaskChain", description="Chain a tree of tasks")
def task_chain(input: Protocol, ptaskchain: PTaskChain) -> PTaskChain:
    """
    PROB: Problem input is a generic protocol, type hints will fail, need to support params not being tied to the protocol name!!!!
    """
