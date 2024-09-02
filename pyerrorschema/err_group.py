from copy import deepcopy
from typing import Any, Dict, List, Optional

from typing_extensions import Self

from .err_base import ErrorSchema


class ErrGroup:
    def __init__(self, error_schemas: Optional[List] = None) -> None:
        if error_schemas and not all(isinstance(err, ErrorSchema) for err in error_schemas):
            raise ValueError("All elements must be instances of ErrorSchema.")
        self._error_schemas: List = error_schemas or []

    @property
    def error_schemas(self) -> List:
        return self._error_schemas

    def copy(self) -> Self:
        """Create a copy of the error group."""
        return self.__class__(self.to_list())

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

    def to_string(self) -> str:
        """Convert the error schemas to a string."""
        return ErrorSchema.wrapping_string(self._error_schemas)

    def to_dict(self) -> List[Dict]:
        """Convert the error schemas to a dictionary."""
        return [err.to_dict() for err in self._error_schemas]

    def to_list(self) -> List:
        """Convert the error schemas to a list."""
        return deepcopy(self._error_schemas)

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
