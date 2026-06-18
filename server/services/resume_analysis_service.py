from services.chat_service import (
    client
)


def analyze_resume(
    resume_text,
    job_description
):

    prompt = f"""
You are an expert recruiter.

Analyze this resume against
the given job description.

Resume:

{resume_text}

Job Description:

{job_description}

Provide:

1. Match Score (0-100)

2. Strengths

3. Missing Skills

4. Resume Improvements

5. Overall Verdict
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