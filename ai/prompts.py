RESUME_ANALYSIS_PROMPT = """
You are an expert HR recruiter.

Analyze the following resume.

Return ONLY valid JSON.

Format:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": "",
    "experience": ""
}}

Resume:

{resume}
"""

QUESTION_PROMPT = """
You are an expert technical interviewer.

Candidate Skills:
{skills}

Generate exactly 10 interview questions.

Rules:
1. Questions should be based ONLY on the candidate's skills.
2. Difficulty should gradually increase (Easy → Medium → Hard).
3. Do not repeat questions.
4. Return ONLY valid JSON.
5. No markdown.

Format:

{{
    "questions": [
        {{
            "question": "...",
            "skill": "...",
            "difficulty": "Easy"
        }}
    ]
}}
"""
EVALUATION_PROMPT = """
You are an expert technical interviewer.

Evaluate the candidate's answer.

Question:
{question}

Candidate Answer:
{answer}

Rules:
1. Score the answer from 0 to 10.
2. Give constructive feedback.
3. Provide the ideal answer.
4. Return ONLY valid JSON.
5. No markdown.

Format:

{{
    "score": 8,
    "feedback": "Good answer but mention inheritance.",
    "ideal_answer": "Object-Oriented Programming is a programming paradigm based on objects..."
}}
"""