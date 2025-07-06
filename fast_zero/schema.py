from datetime import date
from typing import List

from pydantic import BaseModel


class Book(BaseModel):
    name: str
    isbn: str
    author: str
    year_of_lauch: int


class Books(BaseModel):
    books: List[Book]


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
