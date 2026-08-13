import json

from ai.groq_client import ask_groq
from ai.prompts import EVALUATION_PROMPT


def evaluate_answer(question, answer):

    prompt = EVALUATION_PROMPT.format(
        question=question,
        answer=answer
    )

    response = ask_groq(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)

    except Exception as e:
        raise Exception(
            f"Unable to parse AI response.\n\nResponse:\n{response}\n\nError: {e}"
        )