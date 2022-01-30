from enum import Enum

import logging.config
import os
from app.main.util.exceptions.custom_exception import ExceptionWithResponse

APP_LOGGER_NAME = "app_logger"


class Handler(Enum):
    FILE = 'file'
    STDOUT = 'stdout'


def app_logger():
    return logging.getLogger(APP_LOGGER_NAME)


def handle_exception(exception: Exception):
    if not exception.instanceof(ExceptionWithResponse) or exception.logging:
        app_logger().error(str(exception))


def init(log_dir: str, handlers: list) -> None:
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": '%(asctime)s %(message)s',
                "datefmt": '%m/%d/%Y %I:%M:%S %p'
            }
        },
        "handlers": {
            Handler.STDOUT.value: {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            Handler.FILE.value: {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'midnight',
                'utc': True,
                'backupCount': 5,
                'filename': f'{log_dir}/app_manager.log',
                'formatter': 'standard',
            }
        },
        "loggers": {
            APP_LOGGER_NAME: {
                'handlers': [h.value for h in handlers]
            }
        }
    }
    logging.config.dictConfig(cfg)

