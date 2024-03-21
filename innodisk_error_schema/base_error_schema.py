from typing import List, Dict
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    type: str = ""
    loc: List[str] = list()
    msg: str = ""
    input: Dict = dict()
    
    def to_dict(self):
        return self.model_dump()
    
    class Config:
        """Pydantic model configuration."""
        extra = "forbid"  # Raise an error when extra fields are present.
    
    @classmethod
    def database_error(cls, **kwargs):
        """Factory method to create an instance for a database error."""
        defaults = {
            "type": "database_error",
            "msg": "Database operation failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
    
    @classmethod
    def file_error(cls, **kwargs):
        """Factory method to create an instance for a file error."""
        defaults = {
            "type": "file_error",
            "loc": ["request"],
            "msg": "File processing failed.",
        }
        defaults.update(kwargs)
        return cls(**defaults)
