"""Common test fixtures and utilities for PyErrorSchema tests."""

import pytest

from pyerrorschema import ErrorSchema, FastAPIErrorSchema


@pytest.fixture
def error_schema():
    """Fixture providing a basic ErrorSchema instance."""
    return ErrorSchema(type="test_error", msg="Test error message")


@pytest.fixture
def fastapi_error_schema():
    """Fixture providing a basic FastAPIErrorSchema instance."""
    return FastAPIErrorSchema(
        type="test_error",
        msg="Test error message",
        ui_msg="User-friendly test message",
        loc=["test_location"],
        input={"test_key": "test_value"}
    )
