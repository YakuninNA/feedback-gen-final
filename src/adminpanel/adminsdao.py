from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from authservice.usersdao import UsersDAO
from src.database import async_session_maker
from src.authservice.models import User


class AdminsDAO(UsersDAO):
    model = User

    @classmethod
    async def get_any_status(cls, email, field_name):
        try:
            async with async_session_maker() as session:
                query = (
                    select(getattr(cls.model, field_name))
                    .where(cls.model.email == email)
                )
                result = await session.execute(query)
                return result.scalar_one()
        except NoResultFound:
            return None

    @classmethod
    async def change_user_status(cls, email, desired_value, desired_field):
        async with async_session_maker() as session:
            update_values = {desired_field: desired_value}
            query = (
                update(cls.model)
                .where(cls.model.email == email)
                .values(update_values)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()
