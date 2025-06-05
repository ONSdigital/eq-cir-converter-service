"""This module defines custom types used in the EQ CIR Converter Service."""

from collections.abc import Mapping

InputSchema = Mapping[str, object]

# Define the type for the converted schema
ConvertedSchema = dict | list | str
