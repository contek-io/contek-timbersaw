import logging.config
import os
import sys

from contek_timbersaw.timed_rolling_file_handler import TimedRollingFileHandler


def setup():
    logger = logging.getLogger()

    log_format = os.getenv(
        'log_format',
        '%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
    )
    log_root = os.getenv('log_root', os.path.join(os.getcwd(), 'logs'))
    log_rolling = os.getenv('log_rolling', 'MIDNIGHT')
    log_retention_days = int(os.getenv('log_retention_days', '7'))

    formatter = logging.Formatter(log_format)
    retention = log_retention_days * 24 * 60 * 60
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setStream(sys.stdout)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = True

    info_dir = os.path.join(log_root, 'info')
    os.makedirs(info_dir, exist_ok=True)
    info_file_handler = TimedRollingFileHandler(
        info_dir,
        compression_format='gz',
        retention=retention,
        when=log_rolling,
        utc=True,
    )
    info_file_handler.setFormatter(formatter)
    info_file_handler.setLevel(logging.INFO)
    logger.addHandler(info_file_handler)

    error_dir = os.path.join(log_root, 'error')
    os.makedirs(error_dir, exist_ok=True)
    error_file_handler = TimedRollingFileHandler(
        error_dir,
        retention=retention,
        when=log_rolling,
        utc=True,
    )
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
