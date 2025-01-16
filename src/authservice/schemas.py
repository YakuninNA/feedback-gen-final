import re

from fastapi_users import schemas
from pydantic import Field, EmailStr, field_validator


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    username: str
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(
        defaul=...,
        min_length=1,
        max_length=30,
        description="Unique account name, from 1 up to 30 symbols"
    )
    email: EmailStr = Field(
        default=...,
        min_length=1,
        max_length=35,
        description="Interviewer @akvelon email address, up to 35 sybmols"
    )
    name: str = Field(
        default=...,
        min_length=1,
        max_length=25,
        description="First name of the interviewer, from 1 up to 25 symbols"
    )
    surname: str = Field(
        default=...,
        min_length=1,
        max_length=25,
        description="Last name of the interviewer, from 1 up to 25 symbols"
    )
    password: str = Field(
        default=...,
        min_length=6,
        max_length=50,
        description="Account password containing both letters and digits, from 6 up to 50 symbols"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        allowed_domain = "@abc.com"
        if not value.lower().endswith(allowed_domain):
            raise ValueError(f"Email must end with '{allowed_domain}'")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        return value

    pass
