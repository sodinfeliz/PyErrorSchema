import json
from typing import Any, Callable, Dict, List, Optional

from pydantic import Field
from typing_extensions import Self

from ..base.err_base import ErrorSchema
from ..types import MsgType
from ..utils import restrict_arguments


class FastAPIErrorSchema(ErrorSchema):
    loc: List[str] = Field(default_factory=list)
    input: Dict[str, Any] = Field(default_factory=dict)
    ui_msg: Optional[str] = Field(default=None)

    def to_dict(self, target: MsgType = "backend") -> Dict[str, Any]:
        """Convert the error schema to a dictionary.

        If target is "frontend", only the fields `msg` and `input` are included, and
        if `ui_msg` is not None, the field `msg` is overwritten by `ui_msg`. If target
        is "backend", all fields are included, except for `ui_msg`.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            error_dict (dict[str, Any]): The error schema as a dictionary.
        """
        error_dict = self.model_dump()

        if target == "frontend":
            error_dict.pop("loc")
            error_dict.pop("type")
            if error_dict["ui_msg"] is not None:
                error_dict["msg"] = error_dict["ui_msg"]

        error_dict.pop("ui_msg")
        return error_dict

    def to_string(self, target: MsgType = "backend") -> str:
        """Convert the error schema to a string.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            err_str (str): The error schema as a string.
        """
        return json.dumps(self.to_dict(target))

    ### Factory methods ###

    def frontend_variant(self, msg: Optional[str] = None) -> Self:
        """Convert the error schema to a frontend error schema.

        .. caution:: This method will be deprecated in the future.
        """
        modified_schema = self.schema_copy()
        if msg is not None:
            modified_schema.msg = msg
        return modified_schema

    @classmethod
    def _create_error(cls, error_type: str, default_msg: str, **kwargs) -> Self:
        """Base factory method to create an instance for an error."""
        readable_error_type = error_type.replace("_", " ").capitalize()
        msg = kwargs.pop("msg", default_msg)

        if "ui_msg" in kwargs:
            kwargs["ui_msg"] = f"{readable_error_type} occurred while {kwargs['ui_msg']}."

        return cls(
            type=error_type,
            msg=f"{readable_error_type}: {msg}",
            **kwargs,
        )

    @classmethod
    @restrict_arguments("type")
    def validation_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a validation error."""
        return cls._create_error("validation_error", "Validation error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def value_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a value error."""
        return cls._create_error("value_error", "Value error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def docker_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a docker error."""
        return cls._create_error("docker_error", "Docker error occurred.", **kwargs)

    @classmethod
    def customized_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a customized error."""
        error_type = kwargs.pop("type", "customized_error")
        return cls._create_error(error_type, "Customized error occurred.", **kwargs)

    @classmethod
    def from_exception(cls, exception: Exception, **kwargs) -> Self:
        """Factory method to create an instance for an exception."""
        exception_mapping: Dict[type[Exception], Callable[[], Self]] = {
            ValueError: cls.value_error,
            KeyError: cls.value_error,
            FileExistsError: cls.file_error,
            FileNotFoundError: cls.file_error,
        }

        error_factory = exception_mapping.get(type(exception), cls.customized_error)
        if "msg" not in kwargs:
            kwargs["msg"] = str(exception)
        if error_factory.__name__ == "customized_error":
            kwargs["type"] = type(exception).__name__

        return error_factory(**kwargs)
