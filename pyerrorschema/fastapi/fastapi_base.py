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
        return json.dumps(self.to_dict(target))

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
        """

        if "exc" in kwargs:
            msg = str(kwargs.pop("exc"))
            ui_msg = kwargs.pop("msg", default_msg)
        else:
            msg = kwargs.pop("msg", default_msg)
            ui_msg = msg

        if "ui_msg" in kwargs:
            ui_msg = kwargs.pop("ui_msg")
        else:
            ui_msg = ui_msg.capitalize().strip()

        pretty_type = error_type.replace("_", " ").capitalize()
        if not msg.startswith(pretty_type):
            msg = f"{pretty_type}: {msg[0].lower() + msg[1:]}"

        return cls(type=error_type, msg=msg, ui_msg=ui_msg, **kwargs)

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
