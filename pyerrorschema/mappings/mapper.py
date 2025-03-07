from typing import Dict, Optional

from .exceptions import (
    EXCEPTION_MAPPINGS_BASE,
    EXCEPTION_MAPPINGS_FASTAPI,
)

SCHEMA_TO_MAPPINGS = {
    "ErrorSchema": EXCEPTION_MAPPINGS_BASE,
    "FastAPIErrorSchema": EXCEPTION_MAPPINGS_FASTAPI,
}


class ExceptionMapper:
    """Mapper between exception types and error types."""

    _default_schema_name = "ErrorSchema"
    _default_error_type = "runtime_error"

    @classmethod
    def get_mapping(
        cls,
        schema_name: Optional[str] = None,
    ) -> Dict[str, Dict[str, str]]:
        """Get the mapping between exception types and error types."""
        return SCHEMA_TO_MAPPINGS.get(schema_name or cls._default_schema_name, {})

    @classmethod
    def get_error_type(
        cls,
        schema_name: str,
        exc_module: str,
        exc_class: str,
    ) -> str:
        """Get the error type for a given exception type."""
        mapping = cls.get_mapping(schema_name)
        error_type = (
            mapping
            .get(exc_module, {})
            .get(exc_class, cls._default_error_type)
        )
        return error_type

    @classmethod
    def get_error_type_from_exception(
        cls,
        schema_name: str,
        exc: Exception,
    ) -> str:
        """Get the error type for a given exception."""
        return cls.get_error_type(
            schema_name,
            exc.__class__.__module__,
            exc.__class__.__name__,
        )
