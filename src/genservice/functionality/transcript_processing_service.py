import json
from json_repair import repair_json

from src.genservice.functionality.genfunctions import polish_qa, extract_qa, categorize_qa
from src.genservice.functionality.utility import process_json, convert_json_to_dialogue


async def categorized_qa_gen_func(transcript_data: dict, tech_requirements: str, general_requirements: str):
    # Process and extract data
    raw_data = process_json(transcript_data)
    dialogue_data = convert_json_to_dialogue(raw_data)

    # Process and extract requirements as a string
    all_requirements = tech_requirements + general_requirements
    requirements_listed = ""
    for category in all_requirements:
        requirements_listed += f"{category}\n"
    print(requirements_listed)

    # Extract, polish and categorize raw data
    extracted_answers = await extract_qa(dialogue_data)
    polished_answers = await polish_qa(extracted_answers)
    categorized_answers = await categorize_qa(
        polished_answers=polished_answers,
        requirements=requirements_listed)

    # JSON-ify and sort to reduce payload
    corrected_json = repair_json(categorized_answers)
    categorized_answers_json = json.loads(corrected_json)

    # Filter technical ones and soft ones to reduce the payload
    print(categorized_answers_json)
    soft_categorized_answers = [item for item in categorized_answers_json if item['Category'] in general_requirements]
    tech_categorized_answers = [item for item in categorized_answers_json if item['Category'] in tech_requirements]

    return {"soft_categorized_answers": soft_categorized_answers,
            "tech_categorized_answers": tech_categorized_answers}
