from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FeedbackGen(Base):
    __tablename__ = "feedback_section"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reg_time: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    interviewer_username: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    interviewer_full_name: Mapped[str] = mapped_column(String, nullable=False)
    feedback_name: Mapped[str] = mapped_column(String, nullable=False)
    soft_skills: Mapped[str] = mapped_column(String, nullable=False)
    engineering_basics: Mapped[str] = mapped_column(String, nullable=False)
    technical_skills: Mapped[str] = mapped_column(String, nullable=False)