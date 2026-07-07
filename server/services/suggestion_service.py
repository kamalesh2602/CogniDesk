from core.config import settings
from openai import OpenAI

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def generate_questions(text):

    prompt = f"""
Generate 5 useful questions someone might ask
about this document.

Return only the questions.
One per line.

Document:
{text}
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    questions = (
        response
        .choices[0]
        .message
        .content
        .split("\n")
    )

    return [
        q.strip("- ").strip()
        for q in questions
        if q.strip()
    ]