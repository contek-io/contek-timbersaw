import gzip
import os

from contek_timbersaw.delete_old_rotator import DeleteOldRotator


class GZipRotator:

    def __init__(self, retention_days: int) -> None:
        self._delete_old_rotator = DeleteOldRotator(retention_days)

    def __call__(self, source: str, dest: str) -> None:
        self._delete_old_rotator(source, dest)
        if not os.path.isfile(dest):
            return

        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)
