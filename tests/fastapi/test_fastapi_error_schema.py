"""Tests for the FastAPIErrorSchema class."""


from pyerrorschema import FastAPIErrorSchema


def test_fastapi_error_schema_creation():
    """Test basic FastAPIErrorSchema creation."""
    error = FastAPIErrorSchema(
        type="test_error",
        msg="Test message",
        ui_msg="User message",
        loc=["test"],
        input={"key": "value"}
    )
    assert error.type == "test_error"
    assert error.msg == "Test message"
    assert error.ui_msg == "User message"
    assert error.loc == ["test"]
    assert error.input == {"key": "value"}


def test_fastapi_error_schema_to_dict_backend():
    """Test FastAPIErrorSchema to_dict method with backend target."""
    error = FastAPIErrorSchema(
        type="test_error",
        msg="Test message",
        ui_msg="User message"
    )
    error_dict = error.to_dict(target="backend")
    assert error_dict["type"] == "test_error"
    assert error_dict["msg"] == "Test message"
    assert "ui_msg" not in error_dict


def test_fastapi_error_schema_to_dict_frontend():
    """Test FastAPIErrorSchema to_dict method with frontend target."""
    error = FastAPIErrorSchema(
        type="test_error",
        msg="Test message",
        ui_msg="User message",
        input={"key": "value"}
    )
    error_dict = error.to_dict(target="frontend")
    assert error_dict["msg"] == "User message"
    assert error_dict["input"] == {"key": "value"}
    assert "type" not in error_dict


class TestFastAPIErrorSchemaFactoryMethods:
    """Tests for FastAPIErrorSchema factory methods."""

    def test_validation_error(self):
        """Test validation_error factory method."""
        error = FastAPIErrorSchema.validation_error(
            msg="Invalid input",
            ui_msg="Please check your input",
        )
        assert error.type == "validation_error"
        assert "invalid input" in error.msg
        assert error.ui_msg == "Please check your input"

    def test_docker_error(self):
        """Test docker_error factory method."""
        error = FastAPIErrorSchema.docker_error(
            msg="Container failed",
            ui_msg="Operation failed",
            auto_loc=False  # Disable automatic location detection
        )
        assert error.type == "docker_error"
        assert "container failed" in error.msg
        assert error.ui_msg == "Operation failed"


class TestFastAPIErrorSchemaDockerClass:
    """Tests for FastAPIErrorSchema.Docker class."""

    def test_waiting(self):
        """Test Docker.waiting factory method."""
        error = FastAPIErrorSchema.Docker.waiting(container="test-container")
        assert error.type == "docker_error"
        assert "test-container" in error.msg
        assert "waiting" in error.msg

    def test_running(self):
        """Test Docker.running factory method."""
        error = FastAPIErrorSchema.Docker.running(container="test-container")
        assert error.type == "docker_error"
        assert "test-container" in error.msg
        assert "running" in error.msg

    def test_stopping(self):
        """Test Docker.stopping factory method."""
        error = FastAPIErrorSchema.Docker.stopping(container="test-container")
        assert error.type == "docker_error"
        assert "test-container" in error.msg
        assert "stopping" in error.msg.lower()


class TestFastAPIErrorSchemaValidationClass:
    """Tests for FastAPIErrorSchema.Validation class."""

    def test_general(self):
        """Test Validation.general factory method."""
        error = FastAPIErrorSchema.Validation.general(
            action="validating user input"
        )
        assert error.type == "validation_error"
        assert "validating user input" in error.msg.lower()


def test_auto_location():
    """Test automatic location setting."""
    # Test with auto_loc disabled
    error = FastAPIErrorSchema.validation_error(auto_loc=False)
    assert isinstance(error.loc, list)
    assert len(error.loc) == 0

    # Test with auto_loc enabled but with explicit loc
    error = FastAPIErrorSchema.validation_error(
        auto_loc=True,
        loc=["custom_location"]
    )
    assert error.loc == ["custom_location"]
