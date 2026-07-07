from core.config import settings
from openai import OpenAI

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def generate_answer(question, chunks):

    context = "\n\n".join(chunks)

    prompt = f"""
You are a document assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, say:
"I could not find that information in the document."

Context:
{context}

Question:
{question}

Answer:
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