from openai import OpenAI
from core.config import settings

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_summary(text):

    prompt = f"""
Summarize this document.

Return ONLY plain text.

Rules:
- Maximum 5 bullet points
- No markdown
- No headings
- No numbering
- Keep each bullet one sentence

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

    return response.choices[0].message.content