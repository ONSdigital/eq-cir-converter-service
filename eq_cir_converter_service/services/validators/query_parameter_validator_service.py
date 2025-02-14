"""This module contains the query parameter validator service."""

import re, os

from eq_cir_converter_service.config.logging_config import logging
from eq_cir_converter_service.exception import exceptions

logger = logging.getLogger(__name__)


class QueryParameterValidatorService:
    """Service class for validating query parameters."""

    @staticmethod
    def validate_current_target_version(current_version: str, target_version: str) -> None:
        """Validates the current and target version in the request parameters using the regex pattern x.y.z where x, y, z are numbers.
        Also, validates the current and target version against the environment variables.

        Parameters:
        - current_version: The current version of the schema.
        - target_version: The target version of the schema.
        """
        pattern = r"^(\d+\.\d+\.\d+)$"

        if re.match(pattern, current_version):
            logger.info("Current version matches the pattern")

            env_current_version = os.getenv("CURRENT_VERSION", "9.0.0")

            if current_version == env_current_version:
                logger.info("Current version is the expected value %s", env_current_version)
            else:
                logger.error("Current version is not the expected value %s", env_current_version)
                raise exceptions.InvalidCurrentVersionException
        else:
            logger.error("Invalid current version %s", current_version)
            raise exceptions.InvalidCurrentVersionException

        if re.match(pattern, target_version):
            logger.info("Target version matches the pattern")

            env_target_version = os.getenv("TARGET_VERSION", "10.0.0")

            if target_version == env_target_version:
                logger.info("Target version is the expected value %s", env_target_version)
            else:
                logger.error("Target version is not the expected value %s", env_target_version)
                raise exceptions.InvalidTargetVersionException
        else:
            logger.error("Invalid target version %s", target_version)
            raise exceptions.InvalidTargetVersionException
