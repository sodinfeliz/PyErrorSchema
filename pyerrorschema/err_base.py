import json
from typing import Any, Dict, List

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self, TypeVar

from .utils import restrict_arguments

ErrorSchemaType = TypeVar("ErrorSchemaType", bound="ErrorSchema")


class ErrorSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="")
    msg: str = Field(default="")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def to_string(self) -> str:
        """Convert the error schema to a string."""
        return json.dumps(self.to_dict())

    def schema_copy(self) -> Self:
        """Create a deep copy of the error schema."""
        return self.__class__(**self.model_dump())

    @staticmethod
    def wrapping_string(error_schemas: List[ErrorSchemaType]) -> str:
        """Wraps the error schemas in a string representation.

        This method is used to wrap a list of error schemas in a string representation. The resulting string
        is a JSON array of error schemas. The error schemas must be instances of ErrorSchema.

        Args:
            error_schemas (List[ErrorSchema]): List of error schemas.

        .. caution:: This method will be deprecated in the future.
        """
        if isinstance(error_schemas, ErrorSchema):
            error_schemas = [error_schemas]
        if isinstance(error_schemas, list):
            if all(isinstance(err, ErrorSchema) for err in error_schemas):
                return f"[{', '.join(err.to_string() for err in error_schemas)}]"
            else:
                raise ValueError("All elements in the list must be instances of ErrorSchema.")
        else:
            raise ValueError("The argument must be an instance of ErrorSchema or a list of ErrorSchema instances.")

    ### Factory methods ###

    @classmethod
    @restrict_arguments("type")
    def database_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a database error."""
        defaults = {
            "type": "database_error",
            "msg": "Database operation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def file_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a file error."""
        defaults = {
            "type": "file_error",
            "msg": "File processing failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def runtime_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a runtime error."""
        defaults = {
            "type": "runtime_error",
            "msg": "Runtime error occurred.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def parse_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a parse error."""
        defaults = {
            "type": "parse_error",
            "msg": "Parse error occurred.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
