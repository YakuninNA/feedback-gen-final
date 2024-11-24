import json

from arq.connections import RedisSettings, logger
from src.database import get_async_manager
from src.genservice.functionality.feedback_gen_service import feedback_parts_gen_func
from src.genservice.functionality.genfunctions import extract_requirements, interview_name_extract
from src.genservice.functionality.transcript_processing_service import categorized_qa_gen_func
from src.genservice.functionality.utility import (parse_requirements, general_requirements)
from src.genservice.crud import create_feedback
from src.genservice.schemas import FeedbackCreate
from src.genservice.models import FeedbackGen
from src.authservice.models import User


redis_settings = RedisSettings(
    host='localhost',
    port=6379,
    database=0
)


async def process_transcript_task(
    ctx, json_file, requirements, position, username, name, surname, filename, timestamp
):
    logger.info(f"Starting task for user {username}.")
    db=None
    try:
        async with get_async_manager() as db:
            transcript_data = json.loads(json_file)

            tech_requirements = parse_requirements(
                await extract_requirements(requirements)
            )

            interview_name = await interview_name_extract(filename) + timestamp

            categorized_qa = await categorized_qa_gen_func(
                transcript_data=transcript_data,
                tech_requirements=tech_requirements,
                general_requirements=general_requirements,
            )

            processed_data = await feedback_parts_gen_func(
                categorized_qa, position, tech_requirements
            )

            feedback_data = FeedbackCreate(
                interviewer_username=username,
                interviewer_full_name=f"{name} {surname}",
                feedback_name=interview_name,
                soft_skills=processed_data["experience_section"],
                engineering_basics=processed_data["engineering_basics_section"],
                technical_skills=processed_data["technical_skills_section"],
            )

            new_feedback = await create_feedback(db=db, feedback_data=feedback_data)
            await db.commit()

            logger.info(f"Task completed successfully. Feedback ID: {new_feedback.id}")
            return new_feedback.id

    except Exception as e:
        logger.exception(
            f"An error occurred while processing the task for user {username}: {e}."
        )
        if db:
            await db.rollback()
        return None


class WorkerSettings:
    functions = [process_transcript_task]
    redis_settings = redis_settings
    max_jobs = 50
    poll_interval = 1
    timeout = 250
    job_timeout = 1000
    log_level = 'INFO'
