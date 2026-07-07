from services.external_clients import get_openai_client


def generate_interview_questions(
    resume_text,
    job_description
):

    prompt = f"""
You are a senior technical interviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Generate:

1. 5 Technical Questions
2. 3 Behavioral Questions
3. 2 Project-Based Questions

For each question give:
- Question
- Ideal Answer
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