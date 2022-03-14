import logging.config
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from contek_timbersaw.delete_old_rotator import DeleteOldRotator
from contek_timbersaw.gzip_rotator import GZipRotator
from contek_timbersaw.log_namer import LogNamer


def setup():
    logger = logging.getLogger()

    formatter = logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setStream(sys.stdout)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True

    logs_dir = os.getenv('log_root', os.getcwd() + '/logs')
    latest_file = os.getenv('log_latest_file', 'latest.log')
    retention_days = int(os.getenv('log_retention_days', '7'))

    info_dir = logs_dir + '/info'
    os.makedirs(info_dir, exist_ok=True)
    error_dir = logs_dir + '/error'
    os.makedirs(error_dir, exist_ok=True)

    info_file_handler = TimedRotatingFileHandler(
        info_dir + '/' + latest_file,
        when='midnight',
        utc=True,
    )
    info_file_handler.namer = LogNamer(latest_file)
    info_file_handler.rotator = GZipRotator(retention_days)
    info_file_handler.setFormatter(formatter)
    info_file_handler.setLevel(logging.INFO)
    logger.addHandler(info_file_handler)

    error_file_handler = TimedRotatingFileHandler(
        error_dir + '/' + latest_file,
        when='midnight',
        utc=True,
    )
    error_file_handler.namer = LogNamer(latest_file)
    info_file_handler.rotator = DeleteOldRotator(retention_days)
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    logger.addHandler(error_file_handler)

    def handle_exception(type, value, tb):
        logger.exception("Unhandled exception", exc_info=(type, value, tb))

    sys.excepthook = handle_exception
