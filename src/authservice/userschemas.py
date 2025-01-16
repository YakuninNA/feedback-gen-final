import re
from pydantic import Field, EmailStr, field_validator, BaseModel


class UserAuthentication(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Interviewer @abc email address, up to 35 symbols"
    )
    hashed_password: str = Field(
        ...,
        max_length=50,
        description="Account password should contain both letters and digits, from 6 up to 50 symbols"
    )

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("password must include at least one letter.")
        if not re.search(r"\d", value):
            raise ValueError("password must include at least one number.")
        if len(value) < 6:
            raise ValueError("password must be at least 6 digits long.")
        return value

    pass


class UserRegistration(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Unique account name, from 1 up to 30 symbols"
    )
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Interviewer @abc email address, up to 35 symbols"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="First name of the interviewer, from 1 up to 25 symbols"
    )
    surname: str = Field(
        ...,
        min_length=1,
        max_length=25,
        description="Last name of the interviewer, from 1 up to 25 symbols"
    )
    hashed_password: str = Field(
        ...,
        max_length=50,
        description="Account password containing both letters and digits, from 6 up to 50 symbols"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        allowed_domain = "@abc.com"
        if not value.lower().endswith(allowed_domain):
            raise ValueError("please use a company email ending in '@abc.com'.")
        return value

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("password must include at least one letter.")
        if not re.search(r"\d", value):
            raise ValueError("password must include at least one number.")
        if len(value) < 6:
            raise ValueError("password must be at least 6 digits long.")
        return value

    pass
