import logging
import os
from logging.config import dictConfig


def configure_logging():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "root": {
                "level": os.getenv("LOGGING_LEVEL", logging.INFO),
                "handlers": ["stream"],
            },
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(name)-12s %(levelname)-4s %(message)s",
                }
            },
            "handlers": {
                "stream": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "gunicorn.access": {
                    "propagate": True,
                },
                "gunicorn.error": {
                    "propagate": True,
                },
            },
        }
    )
