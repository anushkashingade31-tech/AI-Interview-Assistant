import json

from ai.groq_client import ask_groq
from ai.prompts import RESUME_ANALYSIS_PROMPT


def analyze_resume(resume_text):

    prompt = RESUME_ANALYSIS_PROMPT.format(
        resume=resume_text
    )

    response = ask_groq(prompt)

    # Remove markdown if present
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        data = json.loads(response)
        return data

    except Exception as e:
        raise Exception(
            f"Unable to parse AI response.\n\nResponse:\n{response}\n\nError: {e}"
        )