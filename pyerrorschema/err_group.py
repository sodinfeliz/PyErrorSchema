from copy import deepcopy
from typing import Dict, List, Optional, TypeVar

from typing_extensions import Self

from .err_base import ErrorSchema

ErrorSchemaType = TypeVar("ErrorSchemaType", bound="ErrorSchema")


class ErrGroup:
    def __init__(self, error_schemas: Optional[List[ErrorSchemaType]] = None) -> None:
        self._validate_instance(error_schemas)
        self.error_schemas: List[ErrorSchemaType] = error_schemas or []

    def __len__(self):
        return len(self.error_schemas)

    def __iter__(self):
        return iter(self.error_schemas)

    def __getitem__(self, index):
        return self.error_schemas[index]

    def __setitem__(self, index, value):
        if not isinstance(value, ErrorSchemaType):
            raise ValueError("The error schema must be an instance of ErrorSchema.")
        self.error_schemas[index] = value

    def _validate_instance(self, errs):
        """Check if the error schemas are instances of ErrorSchema."""
        if errs is None:
            return
        if isinstance(errs, list):
            if not all(isinstance(err, ErrorSchema) for err in errs):
                raise ValueError("All elements must be instances of ErrorSchema.")
        elif not isinstance(errs, ErrorSchema):
            raise ValueError("The error schema must be an instance of ErrorSchema.")

    def to_string(self) -> str:
        """Convert the error schemas to a string."""
        return ErrorSchema.wrapping_string(self.error_schemas)

    def to_dict(self) -> List[Dict]:
        """Convert the error schemas to a dictionary."""
        return [err.to_dict() for err in self.error_schemas]

    def to_list(self) -> List:
        """Convert the error schemas to a list."""
        return deepcopy(self.error_schemas)

    def append(self, error_schema: ErrorSchemaType) -> None:
        """Add an error schema to the group."""
        self._validate_instance(error_schema)
        self.error_schemas.append(error_schema)

    def copy(self) -> Self:
        """Create a copy of the error group."""
        return self.__class__(self.to_list())

    def extend(self, error_schemas: List[ErrorSchema]) -> None:
        """Add a list of error schemas to the group."""
        if not isinstance(error_schemas, list):
            raise ValueError("The error_schemas must be a list type.")
        self._validate_instance(error_schemas)
        self.error_schemas.extend(error_schemas)

    def clear(self) -> None:
        """Clear all error schemas from the group."""
        self.error_schemas.clear()
