"""Tests for the FastAPIErrGroup class."""

import pytest

from pyerrorschema import FastAPIErrGroup, FastAPIErrorSchema


@pytest.fixture
def fastapi_error_group():
    """Fixture providing a basic FastAPIErrGroup instance."""
    group = FastAPIErrGroup()
    group.append(
        FastAPIErrorSchema(
            type="error1",
            msg="First error",
            ui_msg="First user error",
            loc=["loc1"],
            input={"key1": "value1"}
        )
    )
    group.append(
        FastAPIErrorSchema(
            type="error2",
            msg="Second error",
            ui_msg="Second user error",
            loc=["loc2"],
            input={"key2": "value2"}
        )
    )
    return group


def test_fastapi_error_group_creation():
    """Test basic FastAPIErrGroup creation."""
    group = FastAPIErrGroup()
    assert len(group) == 0
    assert list(group) == []


def test_fastapi_error_group_append():
    """Test appending errors to group."""
    group = FastAPIErrGroup()
    error = FastAPIErrorSchema(
        type="test_error",
        msg="Test message",
        ui_msg="User message"
    )
    group.append(error)
    assert len(group) == 1
    assert group[0] == error


def test_fastapi_error_group_append_invalid():
    """Test appending invalid error type."""
    group = FastAPIErrGroup()
    with pytest.raises(ValueError, match="must be an instance of FastAPIErrorSchema"):
        group.append("not an error schema")


def test_fastapi_error_group_extend():
    """Test extending group with multiple errors."""
    group = FastAPIErrGroup()
    errors = [
        FastAPIErrorSchema(type="error1", msg="First error"),
        FastAPIErrorSchema(type="error2", msg="Second error")
    ]
    group.extend(errors)
    assert len(group) == 2
    assert all(isinstance(e, FastAPIErrorSchema) for e in group)


def test_fastapi_error_group_extend_with_group():
    """Test extending group with another group."""
    group1 = FastAPIErrGroup()
    group1.append(FastAPIErrorSchema(type="error1", msg="First error"))

    group2 = FastAPIErrGroup()
    group2.append(FastAPIErrorSchema(type="error2", msg="Second error"))

    group1.extend(group2)
    assert len(group1) == 2


def test_fastapi_error_group_to_dict(fastapi_error_group):
    """Test converting group to dict with different targets."""
    # Test backend target
    backend_dicts = fastapi_error_group.to_dicts(target="backend")
    assert len(backend_dicts) == 2
    assert all("type" in d for d in backend_dicts)
    assert all("ui_msg" not in d for d in backend_dicts)

    # Test frontend target
    frontend_dicts = fastapi_error_group.to_dicts(target="frontend")
    assert len(frontend_dicts) == 2
    assert all("type" not in d for d in frontend_dicts)
    assert all("input" in d for d in frontend_dicts)


def test_fastapi_error_group_to_string(fastapi_error_group):
    """Test converting group to string with different targets."""
    # Test backend target
    backend_str = fastapi_error_group.to_string(target="backend")
    assert isinstance(backend_str, str)
    assert "error1" in backend_str
    assert "error2" in backend_str

    # Test frontend target
    frontend_str = fastapi_error_group.to_string(target="frontend")
    assert isinstance(frontend_str, str)
    assert "First user error" in frontend_str
    assert "Second user error" in frontend_str


def test_fastapi_error_group_append_loc(fastapi_error_group):
    """Test appending location to all errors."""
    fastapi_error_group.append_loc("new_loc")
    assert all("new_loc" in err.loc for err in fastapi_error_group)


def test_fastapi_error_group_extend_loc(fastapi_error_group):
    """Test extending locations for all errors."""
    new_locs = ["loc3", "loc4"]
    fastapi_error_group.extend_loc(new_locs)
    assert all(
        all(loc in err.loc for loc in new_locs)
        for err in fastapi_error_group
    )


def test_fastapi_error_group_update_input(fastapi_error_group):
    """Test updating input data for all errors."""
    # Test updating without overwrite
    new_input = {"new_key": "new_value"}
    fastapi_error_group.update_input(new_input)
    assert all(
        err.input.get("new_key") == "new_value"
        for err in fastapi_error_group
    )
    assert all(
        err.input.get("key1") or err.input.get("key2")
        for err in fastapi_error_group
    )

    # Test updating with overwrite
    overwrite_input = {"overwrite_key": "overwrite_value"}
    fastapi_error_group.update_input(overwrite_input, overwrite=True)
    assert all(
        err.input == overwrite_input
        for err in fastapi_error_group
    )
