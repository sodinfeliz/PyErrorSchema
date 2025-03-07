"""
Exception to error type mappings for PyErrorSchema.

This module contains the mappings between exception types and their corresponding
error types. The mappings are organized by module namespace for better organization
and maintainability.
"""

EXCEPTION_MAPPINGS_BASE = {
    "builtins": {
        # File-related
        "FileNotFoundError": "file_error",
        "IsADirectoryError": "file_error",
        "NotADirectoryError": "file_error",
        "PermissionError": "file_error",
        "FileExistsError": "file_error",

        # Value-related
        "ValueError": "value_error",
        "TypeError": "value_error",
        "AttributeError": "value_error",

        # Runtime-related
        "RuntimeError": "runtime_error",
        "NotImplementedError": "runtime_error",
        "ImportError": "runtime_error",
    },
    "psycopg2.errors": {
        "UndefinedTable": "database_error",
    },
}


EXCEPTION_MAPPINGS_FASTAPI = {
    **EXCEPTION_MAPPINGS_BASE,
    "docker.errors": {
        "APIError": "docker_error",
        "ContainerError": "docker_error",
        "DockerException": "docker_error",
        "ImageNotFound": "docker_error",
        "NotFound": "docker_error",
    },
}
