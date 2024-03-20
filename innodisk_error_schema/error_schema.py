from typing import List, Dict
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    type: str = ""
    loc: List[str] = list()
    msg: str = ""
    input: Dict = dict()
    
    def to_dict(self):
        return self.model_dump()


class DatabaseErrorSchema(ErrorSchema):
    type: str = "database_error"
    msg: str = "database failed"


class FileErrorSchema(ErrorSchema):
    type: str = "file_error"
    loc: List[str] = ["request"]
    msg: str = "file failed"


class ValidationErrorSchema(ErrorSchema):
    type: str = "validation_error"


class ValueErrorSchema(ErrorSchema):
    type: str = "value_error"
