from fastapi import FastAPI
from db.mongo import db
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

@app.get("/test-db")
def test_db():
    db.workspaces.insert_one({
        "name": "First Workspace"
    })

    return {"success": True}

from api.workspaces import router as workspace_router

app.include_router(workspace_router)

from api.documents import router as document_router

app.include_router(document_router)

app.include_router(chat_router)

from api.auth import router as auth_router

app.include_router(auth_router)

from api.resume_analyzer import router as resume_router

app.include_router(resume_router)

from api.interview import router as interview_router

app.include_router(interview_router)

from api.resume_rewriter import (
    router as resume_rewriter_router
)

app.include_router(
    resume_rewriter_router
)