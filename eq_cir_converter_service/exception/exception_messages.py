"""This module contains the exception messages for the EQ CIR Converter Service."""

exception_500_schema_processing = "Error encountered while processing the schema"


def exception_400_invalid_version(version_type: str) -> str:
    """Returns the exception message for an invalid version."""
    return f"The {version_type} version must be in the format x.y.z where x, y, z are numbers"


exception_400_empty_input_json = "Input JSON schema is empty"
