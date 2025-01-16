from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_filter(cls, **filer_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filer_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_instance(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
