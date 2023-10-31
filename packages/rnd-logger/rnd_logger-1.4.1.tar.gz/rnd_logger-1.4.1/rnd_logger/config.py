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
                "handlers": ["default"],
            },
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(name)-4s %(levelname)-4s %(message)s",
                },
                "standard": {
                  "format": "%(name)-4s %(levelname)-4s %(message)s"
                }
            },
            "handlers": {
                "json": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": "ext://sys.stdout",
                },
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "gunicorn.access": {
                    "propagate": True,
                    "level": os.getenv("LOGGING_LEVEL", logging.INFO),
                },
                "gunicorn.error": {
                    "propagate": True,
                    "level": os.getenv("LOGGING_LEVEL", logging.INFO),
                },
                "json": {
                    "handlers": ["json"],
                    "level": os.getenv("LOGGING_LEVEL", logging.getLevelName(logging.INFO)),
                    "propagate": True
                },
            },
        }
    )
