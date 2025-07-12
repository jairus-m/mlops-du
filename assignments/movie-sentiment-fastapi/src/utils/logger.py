"""
Module for configuring the logger for the FastAPI app.
"""

import logging.config
import sys
from src.utils import LOG_PATH

# Define logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
            "formatter": "standard",
        },
    },
    "loggers": {
        __name__: {"handlers": ["console", "file"], "level": "INFO", "propagate": True}
    },
}

# Configure logging using dictConfig
logging.config.dictConfig(logging_config)

# Get logger instance
logger = logging.getLogger(__name__)
