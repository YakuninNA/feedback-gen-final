from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.authservice.models import User
from src.authservice.auth_db import get_user_db
from src.config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    def __init__(self, user_db: SQLAlchemyUserDatabase[User, int]):
        super().__init__(user_db)
        self.reset_password_token_secret = SECRET_AUTH
        self.verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.email} has registered.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase[User, int] = Depends(get_user_db)):
    yield UserManager(user_db)
