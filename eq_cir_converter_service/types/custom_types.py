"""This module defines custom types used in the EQ CIR Converter Service."""

from collections.abc import Mapping

# Define a custom type for the schema.
Schema = Mapping[str, object]
