import json

from ai.groq_client import ask_groq


def generate_summary(answers):

    prompt = f"""
You are an expert technical interviewer.

Below are interview results.

{answers}

Write a concise report.

Return ONLY valid JSON.

{{
    "strengths":[
        "...",
        "..."
    ],
    "weaknesses":[
        "...",
        "..."
    ],
    "recommendation":"..."
}}
"""

    response = ask_groq(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    return json.loads(response)