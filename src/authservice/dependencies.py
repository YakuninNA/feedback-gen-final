from fastapi import (
    HTTPException,
    status,
    Request,
    Depends
)

from jose import jwt, JWTError

from src.authservice.models import User
from src.authservice.usersdao import UsersDAO
from src.config import SECRET_AUTH, ALGORYTHM


def get_token(
        request: Request
):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    return token


async def get_current_user(
        token: str = Depends(get_token)
):
    try:
        payload = jwt.decode(token=token, key=SECRET_AUTH, algorithms=ALGORYTHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not valid")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with such ID doesn't exist")

    user = await UsersDAO.find_by_filter(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


async def get_current_admin_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted content")
    return current_user
