from typing import Iterator, List

from ..err_group import ErrGroup
from ..types import MsgType
from .fastapi_base import FastAPIErrorSchema


class FastAPIErrGroup(ErrGroup):
    """A group of FastAPIErrorSchema instances.

    Attributes:
        error_schemas (List[FastAPIErrorSchema]): The list of FastAPIErrorSchema instances.
    """

    def __init__(self) -> None:
        self._error_schemas: List[FastAPIErrorSchema] = []

    def __repr__(self) -> str:
        return f"FastAPIErrGroup(len={len(self)})"

    def __iter__(self) -> Iterator[FastAPIErrorSchema]:
        return iter(self._error_schemas)

    def __getitem__(self, index: int) -> FastAPIErrorSchema:
        return super().__getitem__(index)

    def __setitem__(self, index: int, value: FastAPIErrorSchema) -> None:
        if not isinstance(value, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")
        return super().__setitem__(index, value)

    ## Methods for converting the error schemas ##

    def to_dict(self, target: MsgType = "backend") -> List[dict]:
        """Convert the error schemas to a dictionary.

        .. note:: This method is deprecated. Use `to_dicts` instead.
        """
        return [err.to_dict(target) for err in self._error_schemas]

    def to_dicts(self, target: MsgType = "backend") -> List[dict]:
        """Convert the error schemas to a dictionary."""
        return [err.to_dict(target) for err in self._error_schemas]

    def to_string(self, target: MsgType = "backend") -> str:
        """Convert the error schemas to a string."""
        return f"[{', '.join(err.to_string(target) for err in self._error_schemas)}]"

    ## Methods for modifying the error schemas ##

    def append(self, error_schema: FastAPIErrorSchema) -> None:
        """Add an error schema to the group."""
        if not isinstance(error_schema, FastAPIErrorSchema):
            raise ValueError("The error schema must be an instance of FastAPIErrorSchema.")
        self._error_schemas.append(error_schema)

    def extend(self, error_schemas: List[FastAPIErrorSchema]) -> None:
        """Add a list of error schemas to the group."""
        if not all(isinstance(err, FastAPIErrorSchema) for err in error_schemas):
            raise ValueError("All elements must be instances of FastAPIErrorSchema.")
        self._error_schemas.extend(error_schemas)

    def append_loc(self, loc: str) -> None:
        """Globally append a location to all error schemas in the group."""
        for err in self._error_schemas:
            err.loc.append(loc)
