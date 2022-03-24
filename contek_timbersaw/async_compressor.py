import bz2
import gzip
import logging
import lzma
import os
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class AsyncCompressor:

    def __init__(self, compression_format: str) -> None:
        if compression_format is not None:
            compression_format = compression_format.lower()
        if compression_format == 'gz' or compression_format == 'gzip':
            self._extension = 'gz'
            self._open_out = gzip.open
        elif compression_format == 'bz2' or compression_format == 'bzip2':
            self._extension = 'bz2'
            self._open_out = bz2.open
        elif compression_format == 'lzma':
            self._extension = 'lzma'
            self._open_out = lzma.open
        else:
            self._extension = None
            self._open_out = None
        self._executor = ThreadPoolExecutor(1)

    def __call__(self, source: str, dest: str = None) -> None:
        if self._open_out is None:
            return
        if not os.path.isfile(source):
            return
        if dest is None:
            if self._extension is None:
                raise ValueError('Unknown file extension')
            dest = f"{source}.{self._extension}"
        self._executor.submit(self._gz, source, dest)

    def _gz(self, source: str, dest: str) -> None:
        try:
            f_in = open(source, 'rb')
            f_out = self._open_out(dest, 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            os.remove(source)
        except IOError:
            logger.exception(f"Failed to compress {source} into {dest}.")
