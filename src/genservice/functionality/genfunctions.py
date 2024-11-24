from src.genservice.functionality.few_shot_prompting import (
    QA_EXTRACTION_FSP, QA_POLISH_FSP, QA_CATEGORIZATION_FSP, REQUIREMENTS_EXTRACTION_FSP,
    EXPERIENCE_EXTRACTION_FSP, ENG_BASICS_EXTRACTION_FSP, TECH_SKILLS_EXTRACTION_FSP, INTERVIEW_NAME_EXTRACTION_FSP)

from src.genservice.functionality.prompts import (
    qa_extraction_prompt_func, qa_polish_prompt_func, qa_categorization_prompt_func, requirements_func,
    experience_prompt_func, engineering_basics_prompt_func, technical_skills_prompt_func, interview_name_prompt_func)

from src.genservice.functionality.system_messages import REQUIREMENTS_SYSTEM_MESSAGE, QA_EXTRACTION_SYSTEM_MESSAGE, \
    QA_POLISH_SYSTEM_MESSAGE, QA_CATEGORIZATION_SYSTEM_MESSAGE, EXPERIENCE_SYSTEM_MESSAGE, \
    ENGINEERING_BASICS_SYSTEM_MESSAGE, TECHNICAL_SKILLS_SYSTEM_MESSAGE, INTERVIEW_NAME_EXT_SYSTEM_MESSAGE

from src.genservice.functionality.utility import openai_request_decorator, payload_builder


@openai_request_decorator
async def extract_requirements(requirements: str):
    requirements_extracted_prompt = requirements_func(requirements)

    return payload_builder(
        fsp=REQUIREMENTS_EXTRACTION_FSP,
        prompt=requirements_extracted_prompt,
        system_content=REQUIREMENTS_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=1.0,
        top_p=0.15
        )


@openai_request_decorator
async def extract_qa(processed_data: dict):
    qa_extracted_prompt = qa_extraction_prompt_func(processed_data)

    return payload_builder(
        fsp=QA_EXTRACTION_FSP,
        prompt=qa_extracted_prompt,
        system_content=QA_EXTRACTION_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=0.8,
        top_p=0.25
        )


@openai_request_decorator
async def polish_qa(extracted_answers: str):
    qa_polish_prompt = qa_polish_prompt_func(extracted_answers)

    return payload_builder(
        fsp=QA_POLISH_FSP,
        prompt=qa_polish_prompt,
        system_content=QA_POLISH_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=0.8,
        top_p=0.25
        )


@openai_request_decorator
async def categorize_qa(polished_answers: str, requirements: str):
    qa_categorization_prompt = qa_categorization_prompt_func(polished_answers, requirements)

    return payload_builder(
        fsp=QA_CATEGORIZATION_FSP,
        prompt=qa_categorization_prompt,
        system_content=QA_CATEGORIZATION_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=0.8,
        top_p=0.25
        )


@openai_request_decorator
async def experience_extract(categorized_answers: str, position_name: str):
    experience_extraction_prompt = experience_prompt_func(categorized_answers, position_name)

    return payload_builder(
        fsp=EXPERIENCE_EXTRACTION_FSP,
        prompt=experience_extraction_prompt,
        system_content=EXPERIENCE_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=1.0,
        top_p=0.25
        )


@openai_request_decorator
async def engineering_basics_extract(categorized_answers: str):
    engineering_basics_extraction_prompt = engineering_basics_prompt_func(categorized_answers)

    return payload_builder(
        fsp=ENG_BASICS_EXTRACTION_FSP,
        prompt=engineering_basics_extraction_prompt,
        system_content=ENGINEERING_BASICS_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=1.0,
        top_p=0.25
        )


@openai_request_decorator
async def tech_skills_extract(categorized_answers: str, requirement: str):
    tech_skills_raw_prompt = technical_skills_prompt_func(categorized_answers, requirement)

    return payload_builder(
        fsp=TECH_SKILLS_EXTRACTION_FSP,
        prompt=tech_skills_raw_prompt,
        system_content=TECHNICAL_SKILLS_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=1.0,
        top_p=0.25
        )


@openai_request_decorator
async def interview_name_extract(filename: str):
    interview_name_prompt = interview_name_prompt_func(filename)

    return payload_builder(
        fsp=INTERVIEW_NAME_EXTRACTION_FSP,
        prompt=interview_name_prompt,
        system_content=INTERVIEW_NAME_EXT_SYSTEM_MESSAGE,
        model="gpt-4o-mini-2024-07-18",
        temperature=1.0,
        top_p=0.15
        )