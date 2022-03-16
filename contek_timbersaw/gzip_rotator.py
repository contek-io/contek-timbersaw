import gzip
import logging
import os

from contek_timbersaw.utils import delete_old_files

logger = logging.getLogger(__name__)


class GZipRotator:

    def __init__(self, retention_days: int) -> None:
        self._retention_days = retention_days

    def __call__(self, source: str, dest: str) -> None:
        os.rename(source, dest)
        log_dir = os.path.dirname(dest)
        delete_old_files(log_dir, self._retention_days)

        if not os.path.isfile(dest):
            return
        gz = "%s.gz" % dest
        try:
            f_in = open(dest, 'rb')
            f_out = gzip.open(gz, 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            os.remove(dest)
        except IOError:
            logger.exception(f"Failed to compress {dest} into {gz}.")
