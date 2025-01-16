from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.database import async_session_maker
from src.basedao.basedao import BaseDAO
from src.authservice.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def get_verification_status(cls, email):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.is_verified).where(cls.model.email == email)
                result = await session.execute(query)
                return result.scalar_one()
        except NoResultFound:
            return None
