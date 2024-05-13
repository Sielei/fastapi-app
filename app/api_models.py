"""
This file contains models that are either api response or request json payloads.
"""
from sqlmodel import SQLModel


# properties received when registering a new user
class RegisterUserRequest(SQLModel):
    name: str
    email: str
    password: str


class RegisterUserResponse(SQLModel):
    id: int


class LoginRequest(SQLModel):
    email: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str
