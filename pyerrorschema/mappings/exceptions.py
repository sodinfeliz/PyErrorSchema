"""
Exception to error type mappings for PyErrorSchema.

This module contains the mappings between exception types and their corresponding
error types. The mappings are organized by module namespace for better organization
and maintainability.
"""

EXCEPTION_MAPPINGS_BASE = {
    # Python built-in exceptions
    "builtins": {
        "FileNotFoundError": "file_error",
        "IsADirectoryError": "file_error",
        "NotADirectoryError": "file_error",
        "PermissionError": "file_error",
        "FileExistsError": "file_error",

        "ValueError": "value_error",
        "TypeError": "value_error",
        "AttributeError": "value_error",

        "RuntimeError": "runtime_error",
        "NotImplementedError": "runtime_error",
        "ImportError": "runtime_error",
    },

    "json.decoder": {
        "JSONDecodeError": "value_error",
    },

    "requests.exceptions": {
        "Timeout": "timeout_error",
    },

    # Base exceptions in psycopg2
    "psycopg2": {
        "OperationalError": "database_error",
        "ProgrammingError": "database_error",
        "IntegrityError": "database_error",
        "DataError": "database_error",
        "DatabaseError": "database_error",
        "InterfaceError": "database_error",
        "Warning": "database_error",
    },

    # Exceptions in psycopg2.errors
    "psycopg2.errors": {
        "UndefinedTable": "database_error",
        "ForeignKeyViolation": "database_error",
        "UndefinedColumn": "database_error",
        "UniqueViolation": "database_error",
        "NotNullViolation": "database_error",
    },

    # Exceptions in psycopg2.pool
    "psycopg2.pool": {
        "PoolError": "database_error",
    },
}


EXCEPTION_MAPPINGS_FASTAPI = {
    **EXCEPTION_MAPPINGS_BASE,

    # Exceptions in docker.errors
    "docker.errors": {
        "APIError": "docker_error",
        "ContainerError": "docker_error",
        "DockerException": "docker_error",
        "ImageNotFound": "docker_error",
        "NotFound": "docker_error",
    },

    # Exceptions in Pydantic
    "pydantic_core._pydantic_core": {
        "ValidationError": "validation_error",
    },
}
