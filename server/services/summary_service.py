from services.external_clients import get_openai_client


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

    client = get_openai_client()

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