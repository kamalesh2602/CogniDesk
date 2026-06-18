from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from services.pdf_service import (
    extract_pdf_text
)

from services.resume_analysis_service import (
    analyze_resume
)

import os
import shutil
import uuid

router = APIRouter(
    prefix="/resume-analyzer",
    tags=["Resume Analyzer"]
)


@router.post("/analyze")
async def analyze_resume_endpoint(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):

    upload_dir = "uploads"
    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    temp_filename = (
        f"{uuid.uuid4()}.pdf"
    )

    temp_path = os.path.join(
        upload_dir,
        temp_filename
    )

    with open(
        temp_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume_file.file,
            buffer
        )

    resume_text = extract_pdf_text(
        temp_path
    )

    result = analyze_resume(
        resume_text,
        job_description
    )

    os.remove(temp_path)

    return {
        "analysis": result
    }