import asyncio

from src.genservice.functionality.genfunctions import (experience_extract, engineering_basics_extract,
                                                       tech_skills_extract)


async def feedback_parts_gen_func(categorized_answers: dict, position: str, tech_requirements: str):
    # Process sections (experience, engineering basics, technical skills) concurrently
    experience_section, engineering_basics_section, technical_skills_raw = await asyncio.gather(
        experience_extract(categorized_answers["soft_categorized_answers"], position),
        engineering_basics_extract(categorized_answers["soft_categorized_answers"]),
        tech_skills_extract(categorized_answers["tech_categorized_answers"], tech_requirements))

    return {
        "experience_section": experience_section,
        "engineering_basics_section": engineering_basics_section,
        "technical_skills_section": technical_skills_raw
    }



