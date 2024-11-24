from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    username: str
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    name: str
    surname: str
    password: str
    pass
