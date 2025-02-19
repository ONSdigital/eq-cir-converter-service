import os

def get_current_version_env() -> str:
    """Get the current version from the CURRENT_VERSION environment variable, or use the default value of 9.0.0."""
    return os.getenv("CURRENT_VERSION", "9.0.0")

def get_target_version_env() -> str:
    """Get the target version from the TARGET_VERSION environment variable, or use the default value of 10.0.0."""
    return os.getenv("TARGET_VERSION", "10.0.0")