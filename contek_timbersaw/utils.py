import logging
import os
import time

logger = logging.getLogger(__name__)


def delete_old_files(log_dir: str, retention_days: int) -> None:
    if retention_days <= 0:
        return

    try:
        now = time.time()
        min_modified_time = now - 7 * retention_days
        for f in os.listdir(log_dir):
            file_path = os.path.join(log_dir, f)
            if not os.path.isfile(file_path):
                continue

            stats = os.stat(file_path)
            last_modified = stats.st_mtime
            if last_modified < min_modified_time:
                os.remove(file_path)
    except IOError:
        logger.error(
            f"Failed to delete files older than {retention_days} days")
