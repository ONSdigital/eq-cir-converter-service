"""Configure the logging level for the application."""

import logging

from eq_cir_converter_service.config.config_helpers import get_log_level

logging.basicConfig(
    level=get_log_level(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
