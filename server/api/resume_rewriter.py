from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

import os
import uuid
import shutil

from services.pdf_service import (
    extract_pdf_text
)

from services.resume_rewriter_service import (
    rewrite_resume
)

router = APIRouter(
    prefix="/resume-rewriter",
    tags=["Resume Rewriter"]
)


@router.post("/rewrite")
async def rewrite_resume_endpoint(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    filename = (
        f"{uuid.uuid4()}.pdf"
    )

    path = os.path.join(
        upload_dir,
        filename
    )

    with open(
        path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume_file.file,
            buffer
        )

    resume_text = extract_pdf_text(
        path
    )

    result = rewrite_resume(
        resume_text,
        job_description
    )

    os.remove(path)

    return {
        "result": result
    }