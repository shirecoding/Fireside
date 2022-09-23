__all__ = ["run_in_daemon_thread"]

from threading import Thread
from contextlib import suppress
import logging

from .misc import get_function_import_path

logger = logging.getLogger(__name__)


def run_in_daemon_thread(func, forever: bool = False) -> Thread:
    def daemon():
        if forever:
            while True:
                with suppress(BaseException):
                    func()
        else:
            func()

    thread = Thread(target=daemon, daemon=True)
    logger.debug(f"Starting daemon {get_function_import_path(func) or func} on thread {thread}")
    thread.start()

    return thread
