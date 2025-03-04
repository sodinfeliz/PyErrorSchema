import json
from typing import Any, Dict, List, Optional

from pydantic import Field
from typing_extensions import Self

from ..base.err_base import ErrorSchema
from ..types import MsgType
from ..utils import restrict_arguments


class FastAPIErrorSchema(ErrorSchema):

    ui_msg: Optional[str] = Field(default=None)
    loc: List[str] = Field(default_factory=list)
    input: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self, target: MsgType = "backend") -> Dict[str, Any]:
        """Convert the error schema to a dictionary.

        - For target "backend": include all fields except `ui_msg`.
        - For target "frontend": include only `msg` and `input`. If `ui_msg` is provided,
          its value will override `msg`.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            error_dict (dict[str, Any]): The error schema as a dictionary.
        """

        if target == "frontend":
            return {
                "msg": self.ui_msg or self.msg,
                "input": self.input,
            }

        return self.model_dump(exclude={"ui_msg"})

    def to_string(self, target: MsgType = "backend") -> str:
        """Convert the error schema to a string.

        Args:
            target (MsgType): The target of the error message. The default is "backend".

        Returns:
            err_str (str): The error schema as a string.
        """
        return json.dumps(self.to_dict(target), indent=2)

    ### Factory methods ###

    @classmethod
    def _create_error(
        cls,
        error_type: str,
        default_msg: str,
        **kwargs,
    ) -> Self:
        """Base factory method to create an error schema instance.

        Error message will be formatted as:
        <readable_error_type>: <msg>

        where <readable_error_type> is the error type with underscores replaced
        by spaces and capitalized, e.g. "validation_error" -> "Validation error".

        The priority order for each argument is as follows:

        1. msg (backend message): msg > ui_msg > default_msg
        2. ui_msg (frontend message): ui_msg > msg > default_msg

        The exception message will be appended to the backend message if provided.

        Args:
            error_type (str): The type of the error.
            default_msg (str): The default message of the error.
            **kwargs: Additional keyword arguments including:
                - exc: The exception that occurred.
                - ui_msg: The message to display to the user.
                - msg: The message to display to the backend.

        Returns:
            error_instance (Self): The error schema instance.
        """
        # Extract arguments
        exc = kwargs.pop("exc", None)
        ui_msg = kwargs.pop("ui_msg", None)
        msg = kwargs.pop("msg", default_msg)

        # Format backend message
        backend_msg = msg
        if exc:
            backend_msg += f" ({str(exc)})"

        # Format frontend message
        frontend_msg = (ui_msg or msg).capitalize().strip()

        pretty_type = error_type.replace("_", " ").capitalize()
        if not backend_msg.startswith(pretty_type):
            backend_msg = f"{pretty_type}: {backend_msg[0:1].lower()}{backend_msg[1:]}"

        return cls(type=error_type, msg=backend_msg, ui_msg=frontend_msg, **kwargs)

    @classmethod
    @restrict_arguments("type")
    def validation_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a validation error."""
        return cls._create_error("validation_error", "Validation error occurred.", **kwargs)

    @classmethod
    @restrict_arguments("type")
    def docker_error(cls, **kwargs) -> Self:
        """Factory method to create an instance for a docker error."""
        return cls._create_error("docker_error", "Docker error occurred.", **kwargs)

    ## Subclasses - inherit from ErrorSchema ##

    class File(ErrorSchema.File): ...

    class Map(ErrorSchema.Map): ...

    class DB(ErrorSchema.DB): ...

    class Value(ErrorSchema.Value): ...

    class Parse(ErrorSchema.Parse): ...

    class Runtime(ErrorSchema.Runtime): ...

    class Assumbly(ErrorSchema.Assumbly): ...

    class Unknown(ErrorSchema.Unknown): ...

    ## Subclasses - for FastAPI ##

    class Docker(ErrorSchema.Base): ...
