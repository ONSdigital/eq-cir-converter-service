"""Configure the logging level for the application."""

import logging
import os
from typing import Any


def get_log_level() -> Any:
    """Get the logging level from the LOG_LEVEL environment variable, or use the default value of INFO."""
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    return getattr(logging, log_level)


logging.basicConfig(
    level=get_log_level(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
