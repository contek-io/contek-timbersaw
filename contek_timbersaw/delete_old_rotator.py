import logging
import os
import time

logger = logging.getLogger(__name__)


class DeleteOldRotator:

    def __init__(self, retention_days: int) -> None:
        self._retention_days = retention_days

    def __call__(self, source: str, dest: str) -> None:
        os.rename(source, dest)
        if self._retention_days == 0:
            return

        try:
            log_dir = os.path.dirname(dest)
            now = time.time()
            min_modified_time = now - 7 * self._retention_days
            for f in os.listdir(log_dir):
                file_path = os.path.join(log_dir, f)
                if not os.path.isfile(file_path):
                    continue

                stats = os.stat(file_path)
                last_modified = stats.st_mtime
                if last_modified < min_modified_time:
                    os.remove(file_path)
        except IOError:
            logger.error(f"Failed to delete log files older than {self._retention_days} days")
