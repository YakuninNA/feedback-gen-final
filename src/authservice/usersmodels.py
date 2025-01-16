import enum
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Integer,
    JSON,
    String,
    ForeignKey,
    func,
    text
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped
)

from src.database import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    INTERVIEWER = "INTERVIEWER"


class Role(Base):
    __tablename__ = "roles"
    extend_existing = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    role_name: Mapped[RoleEnum] = mapped_column(
        default=RoleEnum.INTERVIEWER,
        server_default=text("'INTERVIEWER'")
    )
    permission: Mapped[dict | None] = mapped_column(JSON)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    extend_existing = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    reg_time: Mapped[datetime] = mapped_column(server_default=func.now())
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), default=1)

