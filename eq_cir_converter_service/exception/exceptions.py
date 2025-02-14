"""These are the custom exceptions that require pairing with respective exception handling functions to be raised properly."""


class SchemaProcessingException(Exception):
    """This is the Schema Processing exception."""

    pass

class InvalidCurrentVersionException(Exception):
    """This is the Validation exception for request parameters."""

    pass

class InvalidTargetVersionException(Exception):
    """This is the Validation exception for request parameters."""

    pass

class InputJSONValidationException(Exception):
    """This is the Validation exception for empty input JSON."""

    pass

