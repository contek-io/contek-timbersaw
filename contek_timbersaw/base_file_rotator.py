import time
from logging.handlers import TimedRotatingFileHandler

from contek_timbersaw.utils import delete_old_files


class BaseFileRotator:

    def __init__(self, handler: TimedRotatingFileHandler,
                 retention_days: int) -> None:
        self._handler = handler
        self._retention_days = retention_days

    def __call__(self, source=None, dest=None) -> None:
        log_dir = self._handler.baseFilename
        delete_old_files(log_dir, self._retention_days)
        time_tuple = time.gmtime()
        filename = time.strftime(self._handler.suffix, time_tuple) + '.log'
        path = log_dir + '/' + filename
        stream = self._open(path)
        self._handler.close()
        self._handler.setStream(stream)

    def _open(self, filename):
        return open(
            filename,
            self._handler.mode,
            encoding=self._handler.encoding,
            errors=self._handler.errors,
        )
