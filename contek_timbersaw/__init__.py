import logging.config
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from contek_timbersaw.delete_old_rotator import DeleteOldRotator
from contek_timbersaw.gzip_rotator import GZipRotator
from contek_timbersaw.log_namer import LogNamer


def setup():
    logger = logging.getLogger()

    log_format = os.getenv(
        'log_format',
        '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
    )
    log_root = os.getenv('log_root', os.getcwd() + '/logs')
    log_latest_file = os.getenv('log_latest_file', 'latest.log')
    log_retention_days = int(os.getenv('log_retention_days', '7'))

    formatter = logging.Formatter(log_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setStream(sys.stdout)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True

    info_dir = log_root + '/info'
    os.makedirs(info_dir, exist_ok=True)
    error_dir = log_root + '/error'
    os.makedirs(error_dir, exist_ok=True)

    info_file_handler = TimedRotatingFileHandler(
        info_dir + '/' + log_latest_file,
        when='midnight',
        utc=True,
    )
    info_file_handler.namer = LogNamer(log_latest_file)
    info_file_handler.rotator = GZipRotator(log_retention_days)
    info_file_handler.setFormatter(formatter)
    info_file_handler.setLevel(logging.INFO)
    logger.addHandler(info_file_handler)

    error_file_handler = TimedRotatingFileHandler(
        error_dir + '/' + log_latest_file,
        when='midnight',
        utc=True,
    )
    error_file_handler.namer = LogNamer(log_latest_file)
    error_file_handler.rotator = DeleteOldRotator(log_retention_days)
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    logger.addHandler(error_file_handler)

    def handle_exception(exc_type, exc_value, exc_traceback) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.exception(
            "Unhandled exception.",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception
