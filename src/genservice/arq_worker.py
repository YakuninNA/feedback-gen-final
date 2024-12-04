import json

from arq.connections import RedisSettings, logger

from genservice.functionality.few_shot_prompting import (
    few_shot_categorization,
    few_shot_engineering_basics,
    few_shot_extraction,
    few_shot_experience,
    few_shot_interviewer_name,
    few_shot_polish,
    few_shot_requirements,
    few_shot_technical_skills,
)
from genservice.functionality.langchain_pipeline import (
    parse_interviewer_name,
    parse_technical_requirements,
    run_qa_extraction_pipeline,
    run_ti_sections_extraction_pipeline,
)

from src.authservice.models import User
from src.genservice.models import FeedbackGen
from src.database import get_async_manager
from src.genservice.crud import create_feedback
from src.genservice.functionality.utility import general_requirements
from src.genservice.schemas import FeedbackCreate

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

            feedback_name = await parse_interviewer_name(
                transcript_name=filename,
                few_shot_interviewer_name=few_shot_interviewer_name,
                timestamp=timestamp
            )

            all_requirements = await parse_technical_requirements(
                requirements_text=requirements,
                general_requirements=general_requirements,
                few_shot_requirements=few_shot_requirements
            )

            extracted_data = await run_qa_extraction_pipeline(
                processed_data=transcript_data,
                tech_requirements=all_requirements['tech_requirements'],
                general_requirements=all_requirements['general_requirements'],
                categories=all_requirements['all_requirements'],
                few_shot_extraction=few_shot_extraction,
                few_shot_polish=few_shot_polish,
                few_shot_categorization=few_shot_categorization
            )

            feedback_components = await run_ti_sections_extraction_pipeline(
                soft_categorized_answers=extracted_data['soft_categorized_answers'],
                tech_categorized_answers=extracted_data['tech_categorized_answers'],
                position_name=position,
                tech_requirements=all_requirements['tech_requirements'],
                few_shot_experience=few_shot_experience,
                few_shot_engineering_basics=few_shot_engineering_basics,
                few_shot_technical_skills=few_shot_technical_skills
            )

            feedback_data = FeedbackCreate(
                interviewer_username=username,
                interviewer_full_name=f"{name} {surname}",
                feedback_name=feedback_name,
                soft_skills=feedback_components['experience_result'],
                engineering_basics=feedback_components['engineering_result'],
                technical_skills=feedback_components['technical_skills_result']
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
