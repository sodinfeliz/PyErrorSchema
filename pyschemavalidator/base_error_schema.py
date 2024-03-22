from typing import List, Dict
from pydantic import BaseModel, Field


class ErrorSchema(BaseModel):
    type: str = Field(default="")
    loc: List[str] = Field(default_factory=list)
    msg: str = Field(default="")
    input: Dict = Field(default_factory=dict)
    
    def __new__(cls, *args, **kwargs):
        if cls is ErrorSchema:
            raise TypeError("ErrorSchema cannot be instantiated directly!")
        return super().__new__(cls)

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
