import logging
import logging.config
from typing import Any, Dict

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "aiodistbus": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "asyncio": {
            "level": "WARNING",
        },
    },
}


def setup():
    logging.config.dictConfig(LOGGING_CONFIG)
