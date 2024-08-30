from typing import Any, Dict, List, Optional

from pydantic import Field
from typing_extensions import Self

from ..err_base import ErrorSchema
from ..utils import restrict_arguments


class FastAPIErrorSchema(ErrorSchema):
    loc: List[str] = Field(default_factory=list)
    input: Dict[str, Any] = Field(default_factory=dict)

    ### Factory methods ###

    def frontend_variant(self, msg: Optional[str] = None) -> Self:
        """Convert the error schema to a frontend error schema."""
        modified_schema = self.schema_copy()
        if msg is not None:
            modified_schema.msg = msg
        return modified_schema

    @classmethod
    @restrict_arguments("type")
    def validation_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a validation error."""
        defaults: Dict[str, Any] = {
            "type": "validation_error",
            "msg": "Validation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def value_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a value error."""
        defaults: Dict[str, Any] = {
            "type": "value_error",
            "msg": "Value error.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    @restrict_arguments("type")
    def docker_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a docker error."""
        defaults: Dict[str, Any] = {
            "type": "docker_error",
            "msg": "Docker operation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)

    @classmethod
    def customized_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a customized error."""
        return cls(**kwargs)
