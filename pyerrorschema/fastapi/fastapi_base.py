from copy import deepcopy
from typing import Dict, List

from pydantic import Field

from ..err_base import ErrorSchema
from ..utils import restrict_arguments


class FastAPIErrorSchema(ErrorSchema):
    loc: List[str] = Field(default_factory=list)
    input: Dict = Field(default_factory=dict)

    ### Factory methods ###
    
    @classmethod
    @restrict_arguments("type")
    def validation_error(cls, **kwargs):
        """Factory method to create an instance for a validation error."""
        defaults = {
            "type": "validation_error",
            "msg": "Validation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
    
    @classmethod
    @restrict_arguments("type")
    def value_error(cls, **kwargs):
        """Factory method to create an instance for a value error."""
        defaults = {
            "type": "value_error",
            "msg": "Value error.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
    
    @classmethod
    @restrict_arguments("type")
    def docker_error(cls, **kwargs):
        """Factory method to create an instance for a docker error."""
        defaults = {
            "type": "docker_error",
            "msg": "Docker operation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
    
    @classmethod
    def customized_error(cls, **kwargs):
        """Factory method to create an instance for a customized error."""
        return cls(**kwargs)

    @staticmethod
    def frontend_variant(
        error_schema: "FastAPIErrorSchema", 
        text: str = "error"
    ) -> "FastAPIErrorSchema":
        """Convert the error schema to a frontend error schema."""
        new_schema = deepcopy(error_schema)
        new_schema.msg = text
        return new_schema
