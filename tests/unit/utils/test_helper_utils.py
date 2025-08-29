"""Tests for helper utilities."""

import pytest
from fastapi import HTTPException

from eq_cir_converter_service.utils.helper_utils import validate_version


def test_validate_version_valid():
    """Test validate_version with valid semantic versions."""
    # Should not raise for valid semantic versions
    validate_version("1.0.0", "current")
    validate_version("2.1.3-alpha", "target")
    validate_version("0.0.1", "current")


def test_validate_version_invalid():
    """Test validate_version with invalid semantic versions."""
    # Should raise HTTPException for invalid versions
    with pytest.raises(HTTPException) as excinfo:
        validate_version("invalid_version", "current")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail["status"] == "error"
    assert "current" in excinfo.value.detail["message"]

    with pytest.raises(HTTPException) as excinfo:
        validate_version("1.0", "target")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail["status"] == "error"
    assert "target" in excinfo.value.detail["message"]
