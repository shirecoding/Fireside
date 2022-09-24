__all__ = ["run_in_daemon_thread"]

from threading import Thread
import logging
from time import sleep

logger = logging.getLogger(__name__)


def run_in_daemon_thread(func, forever: bool = False) -> Thread:
    def daemon():
        if forever:
            while True:
                try:
                    func()
                except Exception as e:
                    logger.exception(f"Daemon {func} crashed: {e}")
                    sleep(1)
        else:
            func()

    thread = Thread(target=daemon, daemon=True)
    logger.debug(f"Starting daemon {func} on thread {thread}")
    thread.start()

    return thread
