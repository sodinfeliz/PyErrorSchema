"""Tests for the base ErrorSchema class."""


from pyerrorschema import ErrorSchema


def test_error_schema_creation():
    """Test basic ErrorSchema creation."""
    error = ErrorSchema(type="test_error", msg="Test message")
    assert error.type == "test_error"
    assert error.msg == "Test message"


def test_error_schema_to_dict():
    """Test ErrorSchema to_dict method."""
    error = ErrorSchema(type="test_error", msg="Test message")
    error_dict = error.to_dict()
    assert error_dict["type"] == "test_error"
    assert error_dict["msg"] == "Test message"


def test_error_schema_to_string():
    """Test ErrorSchema to_string method."""
    error = ErrorSchema(type="test_error", msg="Test message")
    error_str = error.to_string()
    assert "test_error" in error_str
    assert "Test message" in error_str


class TestErrorSchemaFactoryMethods:
    """Tests for ErrorSchema factory methods."""

    def test_database_error(self):
        """Test database_error factory method."""
        error = ErrorSchema.database_error(msg="Database connection failed")
        assert error.type == "database_error"
        assert "Database connection failed".lower() in error.msg.lower()

    def test_file_error(self):
        """Test file_error factory method."""
        error = ErrorSchema.file_error(msg="File not found")
        assert error.type == "file_error"
        assert "File not found".lower() in error.msg.lower()

    def test_runtime_error(self):
        """Test runtime_error factory method."""
        error = ErrorSchema.runtime_error(msg="Runtime error occurred")
        assert error.type == "runtime_error"
        assert "Runtime error occurred".lower() in error.msg.lower()


class TestErrorSchemaFileClass:
    """Tests for ErrorSchema.File class."""

    def test_not_found(self):
        """Test File.not_found factory method."""
        error = ErrorSchema.File.not_found(path="test.txt")
        assert error.type == "file_error"
        assert "test.txt" in error.msg
        assert "not found" in error.msg.lower()

    def test_already_exists(self):
        """Test File.already_exists factory method."""
        error = ErrorSchema.File.already_exists(path="test.txt")
        assert error.type == "file_error"
        assert "test.txt" in error.msg
        assert "already exists" in error.msg.lower()


class TestErrorSchemaDBClass:
    """Tests for ErrorSchema.DB class."""

    def test_no_results(self):
        """Test DB.no_results factory method."""
        error = ErrorSchema.DB.no_results(desc="querying users")
        assert error.type == "database_error"
        assert "querying users".lower() in error.msg.lower()
        assert "No results found".lower() in error.msg.lower()


def test_from_exception():
    """Test creating ErrorSchema from exception."""
    try:
        raise ValueError("Invalid value")
    except ValueError as exc:
        error = ErrorSchema.from_exception(exc)
        assert error.type == "value_error"
        assert "Invalid value".lower() in error.msg.lower()


def test_list_available_errors():
    """Test listing available error types."""
    errors = ErrorSchema.list_available_errors()
    assert isinstance(errors, list)
    assert "database_error".lower() in errors
    assert "file_error".lower() in errors
