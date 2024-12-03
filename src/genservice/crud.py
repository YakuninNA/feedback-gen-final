from sqlalchemy.ext.asyncio import AsyncSession

from src.genservice.models import FeedbackGen
from src.genservice.schemas import FeedbackCreate


async def create_feedback(db: AsyncSession, feedback_data: FeedbackCreate):
    new_feedback = FeedbackGen(
        interviewer_username=feedback_data.interviewer_username,
        interviewer_full_name=feedback_data.interviewer_full_name,
        feedback_name=feedback_data.feedback_name,
        soft_skills=feedback_data.soft_skills,
        engineering_basics=feedback_data.engineering_basics,
        technical_skills=feedback_data.technical_skills
    )

    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    return new_feedback
