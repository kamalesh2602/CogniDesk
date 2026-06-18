from services.chat_service import client


def rewrite_resume(
    resume_text,
    job_description
):

    prompt = f"""
You are an expert resume reviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:

1. Improved Professional Summary

2. Skills Missing From Resume

3. Rewritten Project Descriptions

4. ATS Optimization Suggestions

5. Final Resume Recommendations

Keep everything structured.
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

    return (
        response
        .choices[0]
        .message
        .content
    )