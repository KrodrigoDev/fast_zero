from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class Book(BaseModel):
    name: str
    isbn: str
    author: str
    year_of_lauch: int


class Books(BaseModel):
    books: List[Book]


# --- Outros ---
class Message(BaseModel):
    message: str


# ---- Users ----


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    birthday: date = date(2003, 7, 25)
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserSchema):
    id: int


class UserPrivate(UserSchema):
    password: str


class ListUsers(BaseModel):
    users: List[UserPublic]
