import json
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from .utils import restrict_arguments


class ErrorSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(default="")
    msg: str = Field(default="")

    def to_dict(self):
        return self.model_dump()

    def to_string(self) -> str:
        """Convert the error schema to a string."""
        return json.dumps(self.to_dict())

    @staticmethod
    def wrapping_string(error_schemas: List["ErrorSchema"]) -> str:
        """Wraps the error schemas in a string representation.

        This method is used to wrap a list of error schemas in a string representation. The resulting string
        is a JSON array of error schemas. The error schemas must be instances of ErrorSchema.

        Args:
            error_schemas (List[ErrorSchema]): List of error schemas.
        """
        if isinstance(error_schemas, ErrorSchema):
            error_schemas = [error_schemas]
        elif isinstance(error_schemas, list):
            if all(isinstance(err, ErrorSchema) for err in error_schemas):
                return f"[{', '.join(err.to_string() for err in error_schemas)}]"
            else:
                raise ValueError("All elements in the list must be instances of ErrorSchema.")
        else:
            raise ValueError("The argument must be an instance of ErrorSchema or a list of ErrorSchema instances.")
        
    ### Factory methods ###

    @classmethod
    @restrict_arguments("type")
    def database_error(cls, **kwargs):
        """Factory method to create an instance for a database error."""
        defaults = {
            "type": "database_error",
            "msg": "Database operation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def file_error(cls, **kwargs):
        """Factory method to create an instance for a file error."""
        defaults = {
            "type": "file_error",
            "msg": "File processing failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
