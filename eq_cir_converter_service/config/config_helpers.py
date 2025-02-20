"""This module contains helper functions for the configuration of the application."""

import logging
import os


def get_log_level() -> int:
    """Get the logging level from the LOG_LEVEL environment variable, or use the default value of INFO."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    return int(getattr(logging, log_level, logging.INFO))


def get_current_version_env() -> str:
    """Get the current version from the CURRENT_VERSION environment variable, or use the default value of 9.0.0."""
    return os.getenv("CURRENT_VERSION", "9.0.0")


def get_target_version_env() -> str:
    """Get the target version from the TARGET_VERSION environment variable, or use the default value of 10.0.0."""
    return os.getenv("TARGET_VERSION", "10.0.0")
