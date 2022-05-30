import logging
import multiprocessing
import os
import time
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
deleter_lock = multiprocessing.Lock()


class AsyncDeleter:

    def __init__(self, log_dir: str, retention: int) -> None:
        self._executor = ThreadPoolExecutor(1)
        self._log_dir = log_dir
        self._retention = retention

    def __call__(self) -> None:
        if self._retention <= 0:
            return

        now = time.time()
        min_modified_time = now - self._retention
        self._executor.submit(self._del, min_modified_time)

    def _del(self, min_modified_time: int) -> None:
        deleter_lock.acquire()

        try:
            for f in os.listdir(self._log_dir):
                file_path = os.path.join(self._log_dir, f)
                if not os.path.isfile(file_path):
                    continue

                stats = os.stat(file_path)
                last_modified = stats.st_mtime
                if last_modified < min_modified_time:
                    os.remove(file_path)
        except (FileNotFoundError, IOError):
            logger.exception(
                f"Failed to delete files modified before {min_modified_time}.")
        finally:
            deleter_lock.release()
