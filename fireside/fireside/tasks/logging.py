__all = ["stdout_logger"]

import logging
from typing import Literal

from fireside.utils.task import task

logger = logging.getLogger(__name__)


@task(name="StdoutLogger", description="Logs to standard output.")
def stdout_logger(
    *, log_level: Literal["debug", "info", "error"] = "debug", **kwargs
) -> None:

    if log_level == "debug":
        logging.debug(kwargs)
    elif log_level == "info":
        logging.info(kwargs)
    elif log_level == "error":
        logging.error(kwargs)
