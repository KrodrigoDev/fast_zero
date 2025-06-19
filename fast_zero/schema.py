from datetime import date
from typing import List

from pydantic import BaseModel


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    birthday: date


class UserPublic(UserSchema):
    id: int


class UserPrivate(UserSchema):
    password: str


class ListUsers(BaseModel):
    users: List[UserPublic]
