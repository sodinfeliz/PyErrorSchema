import inspect
import json
import textwrap
from typing import Any, Dict, List, Optional

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

    @classmethod
    def customized_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a customized error."""
        error_type = kwargs.pop("type", "customized_error")
        return cls._create_error(error_type, "Customized error occurred.", **kwargs)

    ## Subclasses ##

    class Base:
        name: str = "Base"

        @classmethod
        def general(
            cls,
            action: Optional[str] = None,
            reason: Optional[str] = None,
            **kwargs,
        ):
            """General error for a given type.

            Formats the message in one of two ways:
            - "<type> error occurred while <action>."
            - "<type> error occurred since <reason>."

            Args:
                type (str): The type of the error.
                action (str): The action that caused the error.
                reason (str): The reason for the error.
                **kwargs: Additional keyword arguments to pass to the error schema.
            """

            if action and reason:
                raise ValueError("Only one of 'action' or 'reason' should be provided.")

            if action:
                kwargs["msg"] = f"{cls.name} error occurred while {action}."
            else:
                kwargs["msg"] = f"{cls.name} error occurred since {reason}."

            error_method = f"{cls.name.lower()}_error"
            parent_cls = get_parent_class(cls)
            if hasattr(parent_cls, error_method):
                return getattr(parent_cls, error_method)(**kwargs)

            return get_parent_class(cls).customized_error(type=error_method, **kwargs)

    class File(Base):
        name: str = "File"

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
        def writing(cls, path: str, **kwargs):
            """Writing error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"Writing to file '{path}' failed.", **kwargs,
            )

        @classmethod
        def reading(cls, path: str, **kwargs):
            """Reading error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"Reading from file '{path}' failed.", **kwargs,
            )

        @classmethod
        def deleting(cls, path: str, **kwargs):
            """Deleting error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"Deleting file '{path}' failed.", **kwargs,
            )

        @classmethod
        def copying(cls, path: str, **kwargs):
            """Copying error for a given path."""
            return get_parent_class(cls).file_error(
                msg=f"Copying file '{path}' failed.", **kwargs,
            )

    class Map(Base):
        name: str = "Dict"

        @classmethod
        def missing_keys(cls, keys: List[str], **kwargs):
            """Missing keys error for a given keys."""
            return get_parent_class(cls).customized_error(
                type="dict_error",
                msg=f"Keys '{', '.join(keys)}' not found in dictionary.", **kwargs,
            )

    class DB(Base):
        name: str = "Database"

        @classmethod
        def no_result(cls, desc: str, **kwargs):
            """No results when querying a database.

            Format for the message: "No results found while <desc>."
            """
            return get_parent_class(cls).database_error(
                msg=f"No results found while {desc}.", **kwargs,
            )

    class Value(Base):
        name: str = "Value"

    class Parse(Base):
        name: str = "Parse"

    class Runtime(Base):
        name: str = "Runtime"

    class Assumbly(Base):
        name: str = "Assumbly"

    class Unknown(Base):
        name: str = "Unknown"
