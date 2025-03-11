import threading
from functools import lru_cache
from typing import ClassVar, Dict, Final, Optional

from .exceptions import (
    EXCEPTION_MAPPINGS_BASE,
    EXCEPTION_MAPPINGS_FASTAPI,
)

SCHEMA_TO_MAPPINGS = {
    "ErrorSchema": EXCEPTION_MAPPINGS_BASE,
    "FastAPIErrorSchema": EXCEPTION_MAPPINGS_FASTAPI,
}


class ExceptionMapper:
    """Mapper between exception types and error types.

    The mapping structure is organized as:
    {
        'module_name': {
            'exception_class_name': 'error_type'
        }
    }
    """

    _default_schema_name: Final[str] = "ErrorSchema"
    _default_error_type: Final[str] = "runtime_error"
    _valid_schemas: ClassVar[set[str]] = set(SCHEMA_TO_MAPPINGS.keys())
    _lock: ClassVar[threading.Lock] = threading.Lock()
    @classmethod
    def validate_schema(cls, schema_name: str):
        """Validate that the schema name is known."""
        if schema_name not in cls._valid_schemas:
            raise ValueError(
                f"Unknown schema: {schema_name}. "
                f"Valid schemas are: {sorted(cls._valid_schemas)}"
            )

    @classmethod
    def register_schema(
        cls,
        schema_name: str,
        mapping: Dict[str, Dict[str, str]],
    ) -> None:
        """Register a new schema with its mappings.

        Args:
            schema_name: Name of the schema to register
            mappings: Dictionary of module -> class -> error_type mappings
        """
        if schema_name in cls._valid_schemas:
            raise ValueError(
                f"Schema already registered: {sorted(cls._valid_schemas)}. "
                f"Please use a different name."
            )

        with cls._lock:
            cls._valid_schemas.add(schema_name)
            SCHEMA_TO_MAPPINGS[schema_name] = mapping
            cls.clear_caches()

    @classmethod
    @lru_cache(maxsize=None)
    def get_mapping(
        cls,
        schema_name: Optional[str] = None,
    ) -> Dict[str, Dict[str, str]]:
        """Get the mapping between exception types and error types.

        Args:
            schema_name: Optional name of the schema to use. If None, uses default schema.

        Returns:
            Dictionary mapping module names to their exception mappings
        """
        schema_name = schema_name or cls._default_schema_name
        cls.validate_schema(schema_name)
        return SCHEMA_TO_MAPPINGS[schema_name]

    @classmethod
    @lru_cache(maxsize=128)
    def get_error_type(
        cls,
        schema_name: str,
        exc_module: str,
        exc_class: str,
    ) -> str:
        """Get the error type for a given exception type.

        Args:
            schema_name: Name of the schema to use
            exc_module: Module name of the exception
            exc_class: Class name of the exception

        Returns:
            Mapped error type or default error type if no mapping exists
        """
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
        """Get the error type for a given exception.

        Args:
            schema_name: Name of the schema to use
            exc: Exception instance to map

        Returns:
            Mapped error type for the exception
        """
        return cls.get_error_type(
            schema_name,
            exc.__class__.__module__,
            exc.__class__.__name__,
        )

    @classmethod
    def clear_caches(cls):
        """Clear all cached mappings."""
        cls.get_mapping.cache_clear()
        cls.get_error_type.cache_clear()
