import json
from functools import wraps
import markdown
import re
import uuid
import io
from docx import Document
from fastapi.responses import StreamingResponse
from datetime import datetime

from src.genservice.openai_client import client


# JSON to dialogue conversion
def convert_json_to_dialogue(data: dict):
    dialogue = ""

    for item in data:
        sentence = item.get('sentence', '')
        speaker_name = item.get('speaker_name', 'unknown')

        if len(sentence) >= 20:
            if speaker_name == 'speaker 1':
                speaker = "Interviewer"
            elif speaker_name == 'speaker 2':
                speaker = "Candidate"
            else:
                speaker = "Unknown"

            dialogue += f"{speaker}: {sentence}\n"

    return dialogue


# JSON minification
def process_json(data: dict):
    if not isinstance(data, dict):
        return data

    for item in data:
        if isinstance(item, dict):
            item.pop('speaker_id', None)
        else:
            pass

    return data


# OpenAI Request Decorator
def openai_request_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        payload = await func(*args, **kwargs)
        response = await client.chat.completions.create(
            model=payload["model"],
            messages=payload["messages"],
            temperature=payload["temperature"],
            top_p=payload["top_p"]
        )
        print("response has been collected")
        choices = response.choices
        extracted_content = choices[0].message.content

        return extracted_content

    return wrapper


# OpenAI Requirement Handling
def parse_requirements(requirements: str):
    requirements_list = [line.strip(' ') for line in requirements.strip().split('\n') if line]
    categories_listed = []

    for category in requirements_list:
        categories_listed.append(category)

    return categories_listed


# Feedback name incrementation
async def generate_uuid_filename(filename: str):
    return f"{filename}{uuid.uuid4()}"


# Hardcoded variables for sections
general_requirements = [
    "Introduction",
    "Main responsibilities",
    "Git/CI/CD",
    "Scrum/Kanban/Waterfall",
    "SOLID/Object Oriented Programming/Design Patterns"
]


# Markdown formatting func
def preprocess_data(data):
    data = re.sub(r'(:)\s*$', '', data, flags=re.MULTILINE)
    data = re.sub(r'""(.*?)""', r'\1', data, flags=re.DOTALL)
    data = re.sub(r'\n*---\n*', r'\n---\n', data)
    # Commented out to preserve extra newlines
    # data = re.sub(r'\n{3,}', '\n\n', data)
    lines = data.strip().split('\n')

    processed_lines = []

    section_heading_pattern = re.compile(r'^\d+\.\s')
    subheading_pattern = re.compile(r'^###')
    separator_pattern = re.compile(r'^---$')

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            # Optionally, append a line break or a div for empty lines
            processed_lines.append('<br>')
            continue

        if separator_pattern.match(stripped_line):
            processed_lines.append('<hr class="separator">')
            continue

        if section_heading_pattern.match(stripped_line):
            processed_lines.append(f'<div class="level-0 section-heading">{stripped_line}</div>')
            continue

        if subheading_pattern.match(stripped_line):
            processed_lines.append(f'<div class="level-1 subheading">{stripped_line}</div>')
            continue

        processed_lines.append(f'<div class="level-3 content-line">{stripped_line}</div>')
    processed_data = '\n'.join(processed_lines)

    return processed_data


# Markdown converting func
def convert_to_html(data):
    preprocessed_data = preprocess_data(data)
    html = markdown.markdown(
        preprocessed_data,
        extensions=['extra', 'sane_lists', 'codehilite'],
        extension_configs={
            'codehilite': {
                'guess_lang': False
            }
        }
    )
    return html


### High-order payload builder
def payload_builder(fsp: str, prompt: str, system_content: str, model: str, temperature: float, top_p: float):
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": "Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:"},
            {"role": "user", "content": fsp},
            {"role": "user", "content": "Here is the task with the actual data:"},
            {"role": "user", "content": prompt}
        ],
        "top_p": top_p,
        "temperature": temperature
    }

