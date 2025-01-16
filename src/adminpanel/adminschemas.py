from pydantic import Field, EmailStr, field_validator, BaseModel


class UserVerification(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Interviewer @abc email address, up to 35 symbols"
    )
    verification_field: str = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Any given filed in UsersDAO"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        allowed_domain = "@abc.com"
        if not value.lower().endswith(allowed_domain):
            raise ValueError("please use a company email ending in '@abc.com'.")
        return value
    pass


class UserStatusChange(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Interviewer @abc email address, up to 35 symbols"
    )
    db_field: str = Field(
        ...,
        min_length=1,
        max_length=35,
        description="Any given filed in UsersDAO"
    )
    status_field: bool = Field(
        ...,
        description="True/False"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        allowed_domain = "@abc.com"
        if not value.lower().endswith(allowed_domain):
            raise ValueError("please use a company email ending in '@abc.com'.")
        return value

    @field_validator("db_field")
    @classmethod
    def validate_db_field(cls, value: str) -> str:
        allowed_field = "is_"
        if not value.lower().startswith(allowed_field):
            raise ValueError("please use field starting with is_")
        return value

    pass
