from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    interviewer_username: str
    interviewer_full_name: str
    feedback_name: str
    soft_skills: str
    engineering_basics: str
    technical_skills: str
