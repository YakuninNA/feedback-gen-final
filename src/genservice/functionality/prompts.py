import json


def qa_extraction_prompt_func(processed_data: dict):
    return f"""
    Examine this technical interview transcript very carefully:\n{json.dumps(processed_data)}.

    **Expected output:**
    1. Extract all questions asked by the 'Interviewer';
    2. Extract all answers given by the 'Candidate';
    3. Pair each question with its corresponding answer;
    4. Combine questions if they are logically connected;
    5. Combine answers if they are logically connected, relate to the same question;
    6. If the candidate hesitated, didn't know the answer, answered only after a hint - mention it explicitly.

    **Rules:**
    1. Do not make things up, **be strict**;
    2. **Do not exclude** any information from the technical interview transcript;
    3. Do not include any additional information beyond what is provided;
    4. Interviewer entity can only ask questions;
    5. Candidate entity can only provide answers;
    6. Do not mix information from questions to answers.

    **Format:**
    Q: [Extracted Question]
    A: [Extracted Answer]
    """


def qa_polish_prompt_func(processed_data: str):
    return f"""
    Examine this data very carefully: \n{json.dumps(processed_data)}.
    
    **Expected output:**
    1. Extract all relevant information from the answers (A) to the corresponding question (Q);
    2. Ensure the essence and specifics of answers (A) are included, even if the answer is inaccurate;
    3. Provide answers (A) as direct citations with no AI interference;
    4. If the candidate hesitated, didn't know the answer, answered only after a hint - mention explicitly. 
    
    **Rules:**
    1. Ensure each answer (A) is comprehensive, yet no longer than 100 words;
    2. Do not include any additional information beyond what is provided;
    4. Avoid using any advanced vocabulary, speak in simple, human words;
    5. Anonymize all content, avoid using proper names.
        
    **Format:**
    Q: [Extracted Question]
    A: [Extracted Answer]            
    """


def qa_categorization_prompt_func(processed_data: str, categories: str) -> str:
    return f"""
    Examine this data very carefully: \n{json.dumps(processed_data)}.
    Examine the following categories:
    {categories}
    
    **Rules:**
    1. One question (Q) and answer (A) pair can be allocated to only one category;
    2. Use categories as they are provided, **do not alter their names in any way**;
    3. Must not create new categories, use only ones provided in categories;
    4. Output must be valid JSON format with double quotes around keys and string values, ensure proper escaping. 
    """


def requirements_func(requirements: str):
    return f"""
        Examine this data very carefully:\n{json.dumps(requirements)}.

        **Rules:**
        1. Process each requirement line by line;
        2. Ensure include only names of requirements;
        3. Ensure no additional names or symbols are included;
        4. If a requirement is a specific framework - do not enumerate them! Generalize it;
        5. Avoid adding any AI-generated remarks or additional information;
        6. Combine requirements if the topic is similar;
        7. Avoid numeration and bullet points of any kind;
        8. Ensure each requirement on its own line.
    """


def experience_prompt_func(categorized_data: str, position_name: str):
    return f"""
        Examine this data very carefully:\n{json.dumps(categorized_data)}.
         
        **Rules:**
        1. Ensure each section is no longer than 150 words;
        2. Provide a comprehensive summary of the answer using ';' as a separator;
        3. Avoid adding any AI-generated remarks or additional information;
        4. Be strict yet fair, **do not** sugarcoat;
        5. Avoid using any advanced vocabulary, speak in simple words;
        6. Ensure the all names (company, personal names and so on) are anonymized.
            
        **Format:**
        ---
        1. Experience:
        ### **Introduction:**
             - [Extracted Answer] - must be tailored towards **{position_name}** position    
                
        ### **Project Description:**
             - [Extracted Answer] - must be tailored towards **{position_name}** position
        ---
        2. Product Area Impact:
        ### **Main Responsibilities:**
             - [Extracted Bullet 1] - must be tailored towards **{position_name}** position
             - [Extracted Bullet 2] - must be tailored towards **{position_name}** position
             - [Extracted Bullet 3] - must be tailored towards **{position_name}** position
             - [Extracted Bullet 4] - must be tailored towards **{position_name}** position
             - [Extracted Bullet 5] - must be tailored towards **{position_name}** position
        
        ### **Candidate's Position and Main Stack of Technologies:**
             - [Extracted Answer] - must be tailored towards **{position_name}** position    
        ---
        3. Independency:
        ### **Previous Experience/Main Responsibilities (Conclusion):**
             - [Extracted Overview of 1 and 2, indicator of the candidate's independency, 2-3 sentences]
        ---
        4. Proactivity:
        ### **Previous Experience/Main Responsibilities (Conclusion):**
             - [Extracted Overview of 1 and 2, indicator of the candidate's proactivity, 2-3 sentences]
        ---
        5. Mentoring:
        ### **Previous Mentoring Experience:**
             - [Extracted Answer]
        ---
        """


def engineering_basics_prompt_func(categorized_data: str):
    return f"""
        Examine this data very carefully:\n{json.dumps(categorized_data)}.

        **Rules:**
        1. Ensure each section is no longer than 150 words;
        2. Provide a comprehensive summary of the answer using ';' as a separator;
        3. Avoid adding any AI-generated remarks or additional information;
        4. Be strict yet fair, **do not** sugarcoat;
        5. Avoid using any advanced vocabulary, speak in simple words;
        6. Ensure the all names (company, personal names and so on) are anonymized.

        **Format:**
        ---
        ### **Team Size:**
            - [Extracted Overview of the candidate's experience working in teams of different sizes, 3-5 sentences]

        ### **Git Experience, Git Flow Organization, CI/CD:**
            - [Extracted Bullet 1] - candidate's Git experience, 2-3 sentences
            - [Extracted Bullet 2] - candidate's Git Flow experience (how it was organized in their team)
            - [Extracted Bullet 3] - candidate's experience with CI/CD

        ### **Experience with Agile/Scrum/Kanban:**
            - [Extracted Overview of the candidate's experience working with different methodologies, 1-3 sentences]
        ---
        """


def technical_skills_prompt_func(categorized_data: str, requirements: str):
    return f"""
        Examine this data very carefully:\n{json.dumps(categorized_data)}.
                
        **Expected output:**
        1. Make a comprehensive summary of candidate's expertise for each category in {requirements};
        2. If something in {requirements} doesn't appear as a category, the requirement returns [No questions found];

        **Rules:**
        1. Do not use any additional information beyond what is provided in data;
        2. Do not add any additional sections besides categories given in {requirements};
        3. The summary should highlight both strengths and shortcomings of the candidate in regard to a given category;
        4. Avoid using advanced vocabulary, speak in simple terms.

        **Format:**
        ---
        ### **Category 1:**
             - [Insert Summary Here]

        ### **Category 2:**
             - [Insert Summary Here]

        ### **Category 3:**
             - [Insert Summary Here]   
        ---
        """


def interview_name_prompt_func(filename: str):
    return f"""
        Examine this data very carefully:\n{json.dumps(filename)}.

        **Rules:**
        1. Extract only candidate's name and surname.
        """