from typing import Any, List, Optional

from ..err_group import ErrGroup
from .fastapi_base import FastAPIErrorSchema


class FastAPIErrGroup(ErrGroup):
    """A group of FastAPIErrorSchema instances."""
    def __init__(self, error_schemas: Optional[List] = None) -> None:
        super().__init__(error_schemas)
        if error_schemas and not all(isinstance(err, FastAPIErrorSchema) for err in error_schemas):
            raise ValueError("All elements must be instances of FastAPIErrorSchema.")

    def __setitem__(self, index: int, value):
        if not isinstance(value, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")
        return super().__setitem__(index, value)

    def append(self, error_schema: Any) -> None:
        """Add an error schema to the group."""
        if not isinstance(error_schema, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")
        self._error_schemas.append(error_schema)

    def extend(self, error_schemas: List) -> None:
        """Add a list of error schemas to the group."""
        if not all(isinstance(err, FastAPIErrorSchema) for err in error_schemas):
            raise ValueError("All elements must be instances of FastAPIErrorSchema.")
        self._error_schemas.extend(error_schemas)

    def append_loc(self, loc: str) -> None:
        """Globally append a location to all error schemas in the group."""
        for err in self._error_schemas:
            err.loc.append(loc)
