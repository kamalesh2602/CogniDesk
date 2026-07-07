from services.external_clients import get_openai_client


def write_answer(
    question,
    research_notes
):
    client = get_openai_client()
    prompt = f"""
You are an AI research assistant.

Question:
{question}
Conversation History:

{research_notes["conversation_context"]}

Workspace Context:
{research_notes["workspace_context"]}

Web Context:
{research_notes["web_context"]}

Instructions:

1. Answer the user's question directly.

2. Use workspace context when relevant.

3. Use web context only if it helps answer the question.

4. Ignore unrelated information.

5. Do not separately explain
'Workspace Context' and
'Web Context'.

6. Produce one unified answer.

Answer:
"""

    response = (
        client.chat.completions.create(
            model=
            "deepseek/deepseek-chat-v3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
    )