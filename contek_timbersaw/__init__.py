import logging.config
import os
import sys
import time

from contek_timbersaw.timed_rolling_file_handler import TimedRollingFileHandler


def setup():
    log_format = os.getenv(
        'log_format',
        '%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s',
    )
    log_date_format = os.getenv(
        'log_date_format',
        '%Y-%m-%dT%H:%M:%S',
    )
    log_root = os.getenv('log_root', os.path.join(os.getcwd(), 'logs'))
    log_rolling = os.getenv('log_rolling', 'MIDNIGHT')
    log_utc = bool(os.getenv('log_utc', False))
    log_info_retention_days = int(os.getenv('log_info_retention_days', '7'))
    log_warn_retention_days = int(os.getenv('log_error_retention_days', '14'))
    log_error_retention_days = int(os.getenv('log_error_retention_days', '28'))

    logger = logging.getLogger()
    formatter = logging.Formatter(fmt=log_format, datefmt=log_date_format)
    if log_utc:
        formatter.converter = time.gmtime
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setStream(sys.stdout)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True

    def add_file_handler(level, retention_days, compression_format=None):
        file_dir = os.path.join(log_root, level)
        os.makedirs(file_dir, exist_ok=True)
        handler = TimedRollingFileHandler(
            file_dir,
            compression_format=compression_format,
            retention=retention_days * 24 * 60 * 60,
            when=log_rolling,
            utc=log_utc,
        )
        handler.setFormatter(formatter)
        handler.setLevel(logging.getLevelNamesMapping()[level])
        logger.addHandler(handler)

    add_file_handler('INFO', log_info_retention_days, 'gz')
    add_file_handler('WARN', log_warn_retention_days)
    add_file_handler('ERROR', log_error_retention_days)

    def handle_exception(exc_type, exc_value, exc_traceback) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.exception(
            "Unhandled exception.",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception
