import json

from ai.groq_client import ask_groq
from ai.prompts import QUESTION_PROMPT


def generate_questions(skills):

    skill_string = ", ".join(skills)

    prompt = QUESTION_PROMPT.format(
        skills=skill_string
    )

    response = ask_groq(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    data = json.loads(response)

    return data["questions"]