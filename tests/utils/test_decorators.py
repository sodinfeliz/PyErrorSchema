"""Tests for utility decorators."""

import pytest

from pyerrorschema.utils import restrict_arguments


def test_restrict_arguments_decorator():
    """Test the restrict_arguments decorator."""
    @restrict_arguments("forbidden_arg")
    def test_function(**kwargs):
        return kwargs

    # Test with allowed argument
    result = test_function(allowed_arg="value")
    assert result == {"allowed_arg": "value"}

    # Test with forbidden argument
    with pytest.raises(ValueError, match="Overriding the 'forbidden_arg' field is not allowed"):
        test_function(forbidden_arg="value")


def test_restrict_arguments_multiple():
    """Test the restrict_arguments decorator with multiple forbidden arguments."""
    @restrict_arguments("arg1", "arg2")
    def test_function(**kwargs):
        return kwargs

    # Test with allowed argument
    result = test_function(allowed_arg="value")
    assert result == {"allowed_arg": "value"}

    # Test with first forbidden argument
    with pytest.raises(ValueError, match="Overriding the 'arg1' field is not allowed"):
        test_function(arg1="value")

    # Test with second forbidden argument
    with pytest.raises(ValueError, match="Overriding the 'arg2' field is not allowed"):
        test_function(arg2="value")


def test_restrict_arguments_empty():
    """Test the restrict_arguments decorator with no forbidden arguments."""
    @restrict_arguments()
    def test_function(**kwargs):
        return kwargs

    # All arguments should be allowed
    result = test_function(arg1="value1", arg2="value2")
    assert result == {"arg1": "value1", "arg2": "value2"}
