from pydantic import BaseModel,Field
from typing import Literal

class User_registor(BaseModel):
    username: str = Field(max_length=255)
    password: str = Field(max_length=255)
    identify: Literal["admin","user"] = "user"
    allow_login: bool

class User_login(BaseModel):
    username: str = Field(max_length=255)
    password: str = Field(max_length=255)

class User_created(BaseModel):
    username: str
    identify: Literal["admin","user"]