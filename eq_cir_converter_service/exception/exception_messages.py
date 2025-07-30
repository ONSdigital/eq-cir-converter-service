"""This module contains the exception messages for the EQ CIR Converter Service."""

EXCEPTION_500_SCHEMA_PROCESSING = "Error encountered while processing the schema"

EXCEPTION_400_MATCHING_SCHEMA_VERSIONS = (
    "The current and target schema versions are the same - provide different versions"
)

EXCEPTION_400_EMPTY_INPUT_JSON = "Input JSON schema is empty"


def exception_400_invalid_version(version_type: str) -> str:
    """Returns the exception message for an invalid version."""
    return f"The {version_type} version must be in the format x.y.z where x, y, z are numbers"
