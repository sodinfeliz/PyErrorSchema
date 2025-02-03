import inspect
import json
import textwrap
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self, TypeVar

from ..utils import get_parent_class, restrict_arguments

ErrorSchemaType = TypeVar("ErrorSchemaType", bound="ErrorSchema")


class ErrorSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="")
    msg: str = Field(default="")

    def __repr__(self) -> str:
        attrs = [f"{k}={repr(v)}" for k, v in self.__dict__.items() if not k.startswith('_')]
        attrs_str = textwrap.indent(',\n'.join(attrs), '    ')
        return f"{self.__class__.__name__}(\n{attrs_str}\n)"

    def __str__(self) -> str:
        return self.__repr__()

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def to_string(self) -> str:
        """Convert the error schema to a string."""
        return json.dumps(self.to_dict())

    def schema_copy(self) -> Self:
        """Create a deep copy of the error schema."""
        return self.__class__(**self.model_dump())

    @classmethod
    def list_available_errors(cls) -> List[str]:
        """List all available error types."""
        return [
            name
            for name, _ in inspect.getmembers(cls, predicate=inspect.ismethod)
            if name.endswith("_error") and not name.startswith("_")
        ]

    ### Factory methods ###

    @classmethod
    def _create_error(cls, error_type: str, default_msg: str, **kwargs) -> Self:
        """Base factory method to create an instance for an error.

        It will format the error message be like:
        <readable_error_type>: <msg>

        where <readable_error_type> is the error type with underscores replaced
        by spaces and capitalized, e.g. "validation_error" -> "Validation error".
        If the "exc" argument is provided, it will be used as the error message.
        Otherwise, the "msg" argument will be used as the error message.

        Priority order:
        1. exc
        2. msg
        3. default_msg

        Args:
            error_type (str): The type of the error.
            default_msg (str): The default message of the error.
            **kwargs: Additional keyword arguments to pass to the error schema.

        Returns:
            ErrorSchema: The error schema instance.
        """

        if "exc" in kwargs:
            msg = kwargs.pop("exc").__str__()
        else:
            msg = kwargs.pop("msg", default_msg)

        pretty_type = error_type.replace("_", " ").capitalize()
        msg = msg[0].lower() + msg[1:]

        return cls(
            type=error_type,
            msg=f"{pretty_type}: {msg}",
            **kwargs,
        )

    @classmethod
    @restrict_arguments("type")
    def database_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a database error."""
        return cls._create_error("database_error", "Database error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def file_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a file error."""
        return cls._create_error("file_error", "File error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def runtime_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a runtime error."""
        return cls._create_error("runtime_error", "Runtime error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def parse_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a parse error."""
        return cls._create_error("parse_error", "Parse error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def value_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a value error."""
        return cls._create_error("value_error", "Value error occurred.", **kwargs)

    ## Subclasses ##

    class File:

        @classmethod
        def not_found(cls, path: str, **kwargs):
            """File not found error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"File '{path}' not found.", **kwargs,
            )

        @classmethod
        def already_exists(cls, path: str, **kwargs):
            """File already exists error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"File '{path}' already exists.", **kwargs,
            )

        @classmethod
        def general(cls, desc: str, **kwargs):
            """General file error.

            Format for the message: "File operation failed while <desc>."
            """
            return get_parent_class(cls).file_error(
                msg=f"File operation failed while {desc}.", **kwargs,
            )

    class DB:

        @classmethod
        def no_result(cls, desc: str, **kwargs):
            """No results when querying a database.

            Format for the message: "No results found while <desc>."
            """
            return get_parent_class(cls).database_error(
                msg=f"No results found while {desc}.", **kwargs,
            )

        @classmethod
        def general(cls, desc: str, **kwargs):
            """General database error.

            Format for the message: "Database operation failed while <desc>."
            """
            return get_parent_class(cls).database_error(
                msg=f"Database failed while {desc}.", **kwargs,
            )
