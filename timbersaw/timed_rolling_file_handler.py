import os
import time
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

from timbersaw.async_compressor import AsyncCompressor
from timbersaw.async_deleter import AsyncDeleter


class TimedRollingFileHandler(TimedRotatingFileHandler):

    def __init__(
            self,
            log_dir: str,
            file_suffix: str = '.log',
            compression_format: Optional[str] = None,
            retention: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(log_dir, delay=True, **kwargs)
        self._log_dir = log_dir
        self._file_suffix = file_suffix
        self._compress = AsyncCompressor(compression_format)
        self._delete = AsyncDeleter(log_dir, retention)
        self._update_current_file()

    def doRollover(self):
        self.close()
        self._update_current_file()
        self._calculate_new_rollover_at()

    def _calculate_new_rollover_at(self) -> None:
        current_time = int(time.time())
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval

        if self._should_adjust_for_dst_change():
            dst_now = time.localtime(current_time)[-1]
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend

        self.rolloverAt = new_rollover_at

    def _should_adjust_for_dst_change(self) -> bool:
        if self.utc:
            return False
        return self.when == 'MIDNIGHT' or self.when.startswith('W')

    def _update_current_file(self) -> None:
        if self.utc:
            time_tuple = time.gmtime()
        else:
            time_tuple = time.localtime()

        time_str = time.strftime(self.suffix, time_tuple)
        file_name = time_str + self._file_suffix
        new_file = os.path.join(self._log_dir, file_name)
        if self.baseFilename is not None:
            if new_file == self.baseFilename:
                return
            self._compress(self.baseFilename)
        self.baseFilename = new_file
