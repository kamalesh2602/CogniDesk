from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from db.mongo import db

from api.auth import router as auth_router
from api.chat import router as chat_router
from api.documents import router as document_router
from api.interview import router as interview_router
from api.resume_analyzer import router as resume_router
from api.resume_rewriter import router as resume_rewriter_router
from api.workspaces import router as workspace_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting CogniDesk Backend...")
    os.makedirs(
    settings.UPLOAD_DIR,
    exist_ok=True
)
    yield
    print("Shutting down CogniDesk Backend...")


app = FastAPI(
    title="CogniDesk API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "api": "running",
    }


@app.get("/test-db")
def test_db():
    db.workspaces.insert_one(
        {"name": "First Workspace"}
    )
    return {"success": True}


app.include_router(auth_router)
app.include_router(workspace_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(resume_rewriter_router)