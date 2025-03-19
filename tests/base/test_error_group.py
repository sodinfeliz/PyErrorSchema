"""Tests for the ErrGroup class."""

import pytest

from pyerrorschema import ErrGroup, ErrorSchema


@pytest.fixture
def error_group():
    """Fixture providing a basic ErrGroup instance."""
    group = ErrGroup()
    group.append(ErrorSchema(type="error1", msg="First error"))
    group.append(ErrorSchema(type="error2", msg="Second error"))
    return group


def test_error_group_creation():
    """Test basic ErrGroup creation."""
    group = ErrGroup()
    assert len(group) == 0
    assert list(group) == []


def test_error_group_append():
    """Test appending errors to group."""
    group = ErrGroup()
    error = ErrorSchema(type="test_error", msg="Test message")
    group.append(error)
    assert len(group) == 1
    assert group[0] == error


def test_error_group_extend():
    """Test extending group with multiple errors."""
    group = ErrGroup()
    errors = [
        ErrorSchema(type="error1", msg="First error"),
        ErrorSchema(type="error2", msg="Second error")
    ]
    group.extend(errors)
    assert len(group) == 2
    assert group[0] == errors[0]
    assert group[1] == errors[1]


def test_error_group_extend_with_group():
    """Test extending group with another group."""
    group1 = ErrGroup()
    group1.append(ErrorSchema(type="error1", msg="First error"))

    group2 = ErrGroup()
    group2.append(ErrorSchema(type="error2", msg="Second error"))

    group1.extend(group2)
    assert len(group1) == 2


def test_error_group_extend_invalid():
    """Test extending group with invalid type."""
    group = ErrGroup()
    with pytest.raises(ValueError, match="must be a list"):
        group.extend("not a list or group")


def test_error_group_copy(error_group):
    """Test copying error group."""
    copied = error_group.copy()
    assert len(copied) == len(error_group)
    assert copied is not error_group
    assert all(a == b for a, b in zip(copied, error_group))


def test_error_group_clear(error_group):
    """Test clearing error group."""
    assert len(error_group) > 0
    error_group.clear()
    assert len(error_group) == 0


def test_error_group_to_dicts(error_group):
    """Test converting group to list of dictionaries."""
    dicts = error_group.to_dicts()
    assert isinstance(dicts, list)
    assert all(isinstance(d, dict) for d in dicts)
    assert len(dicts) == len(error_group)


def test_error_group_to_string(error_group):
    """Test converting group to string."""
    string = error_group.to_string()
    assert isinstance(string, str)
    assert "error1" in string
    assert "error2" in string


def test_error_group_to_list(error_group):
    """Test converting group to list."""
    error_list = error_group.to_list()
    assert isinstance(error_list, list)
    assert len(error_list) == len(error_group)
    assert all(isinstance(e, ErrorSchema) for e in error_list)


def test_error_group_concat_messages(error_group):
    """Test concatenating error messages."""
    concat = error_group.concat_messages()
    assert "First error" in concat
    assert "Second error" in concat


def test_error_group_contains_type(error_group):
    """Test checking if group contains error type."""
    assert error_group.contains_type("error1")
    assert error_group.contains_type("error2")
    assert not error_group.contains_type("nonexistent_error")


def test_error_group_has_errors(error_group):
    """Test checking if group has errors."""
    assert error_group.has_errors()
    error_group.clear()
    assert not error_group.has_errors()


def test_error_group_iteration(error_group):
    """Test iterating over error group."""
    errors = list(error_group)
    assert len(errors) == 2
    assert all(isinstance(e, ErrorSchema) for e in errors)


def test_error_group_indexing(error_group):
    """Test accessing errors by index."""
    assert isinstance(error_group[0], ErrorSchema)
    assert error_group[0].type == "error1"
    assert error_group[1].type == "error2"


def test_error_group_setitem():
    """Test setting error by index."""
    group = ErrGroup()
    error1 = ErrorSchema(type="error1", msg="First error")
    error2 = ErrorSchema(type="error2", msg="Second error")

    group.append(error1)
    group[0] = error2
    assert group[0] == error2


def test_error_group_setitem_invalid():
    """Test setting invalid type by index."""
    group = ErrGroup()
    group.append(ErrorSchema(type="error1", msg="First error"))

    with pytest.raises(ValueError, match="must be an instance of ErrorSchema"):
        group[0] = "not an error schema"
