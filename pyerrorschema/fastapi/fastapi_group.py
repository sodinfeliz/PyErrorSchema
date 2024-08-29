from typing import List, Optional

from typing_extensions import Self, TypeVar

from ..err_group import ErrGroup
from .fastapi_base import ErrorSchema, FastAPIErrorSchema

ErrorSchemaType = TypeVar("ErrorSchemaType", bound="ErrorSchema")


class FastAPIErrGroup(ErrGroup):
    """A group of FastAPIErrorSchema instances."""

    def __setitem__(self, index, value):
        if not isinstance(value, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")
        return super().__setitem__(index, value)

    def _validate_instance(self, errs):
        """Check if the error schemas are instances of FastAPIErrorSchema."""
        if errs is None:
            return
        if isinstance(errs, list):
            if not all(isinstance(err, FastAPIErrorSchema) for err in errs):
                raise ValueError("All elements must be instances of FastAPIErrorSchema.")
        elif not isinstance(errs, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")

    def append_loc(self, loc: str) -> None:
        """Globally append a location to all error schemas in the group."""
        for err in self.error_schemas:
            err.loc.append(loc)
