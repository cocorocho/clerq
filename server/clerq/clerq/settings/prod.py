from .base import *

import os

DEBUG = False

ALLOWED_HOSTS = [
    os.getenv("DOMAIN"),
]

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        }
    },
    "filters": {"require_debug_true": {"()": "django.utils.log.RequireDebugTrue"}},
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "logfile": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "debug.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "logfile"],
            "propagate": True,
        }
    },
}
