"""This module defines custom types used in the EQ CIR Converter Service."""

from collections.abc import Mapping
from typing import Any

# The type for the input schema, the 'Any' type is used to allow for any value type in the dictionary since the questionnaire schema can be complex
InputSchema = Mapping[str, Any]

# Define the type for the converted schema
ConvertedSchema = dict[str, bool | int | str | list | object]
