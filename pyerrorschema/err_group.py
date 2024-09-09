from copy import deepcopy
from typing import Any, Dict, List

from typing_extensions import Self

from .err_base import ErrorSchema


class ErrGroup:
    def __init__(self) -> None:
        self._error_schemas: List = []

    @property
    def error_schemas(self) -> List:
        return self._error_schemas

    def copy(self) -> Self:
        """Create a copy of the error group."""
        return deepcopy(self)

    def clear(self) -> None:
        """Clear all error schemas from the group."""
        self._error_schemas.clear()

    def __len__(self) -> int:
        return len(self._error_schemas)

    def __iter__(self):
        return iter(self._error_schemas)

    def __getitem__(self, index):
        return self._error_schemas[index]

    def __setitem__(self, index: int, value) -> None:
        if not isinstance(value, ErrorSchema):
            raise ValueError("The error schema must be an instance of ErrorSchema.")
        self._error_schemas[index] = value

    ## Methods for converting the error schemas ##

    def to_dict(self) -> List[Dict]:
        """Convert the error schemas to a dictionary."""
        return [err.to_dict() for err in self._error_schemas]

    def to_string(self) -> str:
        """Convert the error schemas to a string."""
        return f"[{', '.join(err.to_string() for err in self._error_schemas)}]"

    def to_list(self) -> List:
        """Convert the error schemas to a list."""
        return deepcopy(self._error_schemas)

    ## Methods for modifying the error schemas ##

    def append(self, error_schema: Any) -> None:
        """Add an error schema to the group."""
        if not isinstance(error_schema, ErrorSchema):
            raise ValueError("The error schema must be an instance of ErrorSchema.")
        self._error_schemas.append(error_schema)

    def extend(self, error_schemas: List) -> None:
        """Add a list of error schemas to the group."""
        if not all(isinstance(err, ErrorSchema) for err in error_schemas):
            raise ValueError("All elements must be instances of ErrorSchema.")
        self._error_schemas.extend(error_schemas)

    ## Other utility methods ##

    def contains_type(self, error_type: str) -> bool:
        """Check if the error group contains an error schema with a specific type."""
        return any(err.type == error_type for err in self._error_schemas)
