from passlib.context import CryptContext
from jose import jwt
from datetime import timedelta, timezone, datetime
from pydantic import EmailStr

from src.authservice.usersdao import UsersDAO
from src.config import SECRET_AUTH, ALGORYTHM

hashing_context = CryptContext(
    schemes=["bcrypt"]
)


def get_hashed_pwd(password: str) -> str:
    return hashing_context.hash(
        password
    )


def verify_pwd(plain_password: str, hashed_pwd: str) -> bool:
    return hashing_context.verify(
        plain_password,
        hashed_pwd
    )


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    exp_time = datetime.now(timezone.utc) + timedelta(days=1)
    data_to_encode.update(
        {"exp": exp_time}
    )
    encoded_jwt = jwt.encode(
        claims=data_to_encode,
        key=SECRET_AUTH,
        algorithm=ALGORYTHM
    )
    return encoded_jwt


async def authenticate_user(
        email: EmailStr,
        password: str,
):
    user = await UsersDAO.find_by_filter(
        email=email,
    )
    if not user or not verify_pwd(plain_password=password, hashed_pwd=user.hashed_password):
        return None
    return user
