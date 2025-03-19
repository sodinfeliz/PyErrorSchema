"""Tests for the ExceptionMapper class."""

import pytest

from pyerrorschema.mappings import ExceptionMapper


def test_validate_schema_valid():
    """Test schema validation with valid schema name."""
    ExceptionMapper.validate_schema("ErrorSchema")
    ExceptionMapper.validate_schema("FastAPIErrorSchema")


def test_validate_schema_invalid():
    """Test schema validation with invalid schema name."""
    with pytest.raises(ValueError, match="Unknown schema"):
        ExceptionMapper.validate_schema("InvalidSchema")


def test_get_mapping():
    """Test getting exception mappings."""
    mapping = ExceptionMapper.get_mapping("ErrorSchema")
    assert isinstance(mapping, dict)
    assert len(mapping) > 0


def test_get_mapping_default():
    """Test getting default exception mappings."""
    mapping = ExceptionMapper.get_mapping()
    assert isinstance(mapping, dict)
    assert len(mapping) > 0


def test_get_error_type():
    """Test getting error type for specific exception."""
    error_type = ExceptionMapper.get_error_type(
        "ErrorSchema",
        "builtins",
        "ValueError"
    )
    assert error_type == "value_error"


def test_get_error_type_unknown():
    """Test getting error type for unknown exception."""
    error_type = ExceptionMapper.get_error_type(
        "ErrorSchema",
        "unknown_module",
        "UnknownError"
    )
    assert error_type is None


def test_get_error_type_from_exception():
    """Test getting error type from exception instance."""
    try:
        raise ValueError("Test error")
    except ValueError as exc:
        error_type = ExceptionMapper.get_error_type_from_exception(
            "ErrorSchema",
            exc
        )
        assert error_type == "value_error"


def test_get_error_type_from_exception_invalid():
    """Test getting error type from invalid exception."""
    with pytest.raises(TypeError, match="Expected Exception"):
        ExceptionMapper.get_error_type_from_exception(
            "ErrorSchema",
            "not an exception"
        )


def test_clear_caches():
    """Test clearing mapper caches."""
    # First, populate the cache
    ExceptionMapper.get_mapping("ErrorSchema")
    ExceptionMapper.get_error_type("ErrorSchema", "builtins", "ValueError")

    # Clear caches
    ExceptionMapper.clear_caches()

    # Verify cache is cleared by checking internal cache info
    assert ExceptionMapper.get_mapping.cache_info().currsize == 0
    assert ExceptionMapper.get_error_type.cache_info().currsize == 0
