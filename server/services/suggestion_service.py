from services.external_clients import get_openai_client

def generate_questions(text):

    prompt = f"""
Generate 5 useful questions someone might ask
about this document.

Return only the questions.
One per line.

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