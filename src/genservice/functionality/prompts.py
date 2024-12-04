qa_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_extraction}

Examine this technical interview transcript very carefully:
{processed_data}

**Rules:**
1. Extract all questions posed by the Interviewer;
2. Extract all answers provided by the Candidate;
3. Pair each question with its corresponding answer;
4. Consolidate questions that are logically connected;
5. Consolidate answers that are logically connected and pertain to the same question;
6. Explicitly note if the Candidate hesitated, was unsure of the answer, or responded only after receiving a hint;
7. **Do not fabricate any information;** be strict;
8. **Do not exclude any information from the technical interview transcript;**
9. **Do not include any additional information beyond what is provided;**
10. **Ensure the Interviewer entity only asks questions;**
11. **Ensure the Candidate entity only provides answers;**
12. **Do not mix information from questions with answers.**

**Output Format:**
Output must be valid JSON format with double quotes around keys and string values, ensure proper escaping:

[
  {{
    "Interviewer": [Interviewer's question here]",
    "Candidate": [Candidate's answer here]
  }}
]   
...
"""

qa_polish_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_polish}

Examine this data very carefully:
{qa_extracted_data}

**Rules:**
1. **Extract all relevant information from the Candidate's answers to the corresponding Interviewer's questions;**
2. Ensure the essence and specifics of the Candidate's answers are included, even if the answer is inaccurate;
3. Provide the Candidate's answers as direct citations with no AI interference;
4. **Explicitly mention if the Candidate hesitated, was unsure of the answer, or responded only after receiving a hint;**
5. Ensure each Candidate's answer is comprehensive yet no longer than 150 words;
6. **Do not include any additional information beyond what is provided;**
7. Avoid using any advanced vocabulary; speak in simple, human words;
8. **Anonymize all content; avoid using proper names.**

**Output Format:**
Output must be valid JSON format with double quotes around keys and string values, ensure proper escaping:

[
  {{
    "Interviewer": [Interviewer's question here]",
    "Candidate": [Candidate's answer here]
  }}
]   
...
"""

qa_categorization_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_categorization}

Examine this data very carefully: 
{qa_polished_data}

Examine the following categories:
{categories}

**Rules:**
1. Each Interviewer's question and Candidate's answer pair can be allocated to only one category;
2. **Use the provided category names exactly as given; do not alter their names in any way;**
3. **Do not create new categories; use only those provided.**

**Output Format:**
Output must be valid JSON format with double quotes around keys and string values, ensure proper escaping:

[
  {{
    "Interviewer": [Interviewer's question here]",
    "Candidate": [Candidate's answer here]
  }}
]   
...
"""

requirements_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_requirements}

Examine this data very carefully:
{requirements}
 
**Rules:**
1. Process each requirement sequentially, line by line;
2. **Include only the names of the requirements;**
3. **Do not include any additional names or symbols;**
4. If a requirement specifies a particular framework, generalize it instead of enumerating;
5. **Avoid adding any AI-generated remarks or additional information;**
6. Consolidate requirements with similar topics;
7. **Do not use numbering or bullet points of any kind;**
8. Ensure each requirement is on a separate line.
"""

engineering_basics_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_engineering_basics}

Examine this data very carefully:
{soft_categorized_answers}

**Rules:**
1. Ensure each section is no longer than 150 words;
2. **Provide a comprehensive summary of the answer using ';' as a separator;**
3. **Avoid adding any AI-generated remarks or additional information;**
4. **Be strict yet fair; do not sugarcoat;**
5. Avoid using any advanced vocabulary; speak in simple words;
6. **Ensure all names (company, personal names, etc.) are anonymized.**

**Output Format:**
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

technical_skills_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_technical_skills}

Examine this data very carefully:
{tech_categorized_answers}

**Rules:**
1. Make a comprehensive summary of the Candidate's expertise for each category in {tech_requirements};
2. **If a category in {tech_requirements} does not appear examined data, return [No questions asked];**
3. **Do not use any additional information beyond what is provided in the examined data;**
4. **Do not add any additional sections besides the categories provided in {tech_requirements};**
5. The summary should highlight both strengths and shortcomings of the Candidate regarding each category;
6. Avoid using advanced vocabulary; speak in simple terms.

**Output Format:**
---
### **Category 1:**
     - [Insert Summary Here]
### **Category 2:**
     - [Insert Summary Here]
### **Category 3:**
     - [Insert Summary Here]   
---
"""

experience_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_experience}

Examine this data very carefully:
{soft_categorized_answers}

**Rules:**
1. Ensure each section is no longer than 150 words;
2. **Provide a comprehensive summary of the answer using ';' as a separator;**
3. **Avoid adding any AI-generated remarks or additional information;**
4. **Be strict yet fair; do not sugarcoat;**
5. Avoid using any advanced vocabulary; speak in simple words;
6. **Ensure all names (company, personal names, etc.) are anonymized.**

**Output Format:**
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

interviewer_name_extraction_prompt_template = """
Below is an example of the expected format. Do not quote this example in your response. Instead, follow this structure:
{few_shot_interviewer_name}

Examine this data very carefully:
{transcript_name}

**Rules:**
1. Extract only candidate's name and surname.
"""

