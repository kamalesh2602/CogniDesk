from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from db.mongo import db

print("1 - main imported")

from contextlib import asynccontextmanager
print("2")

from fastapi import FastAPI
print("3")

from api.chat import router as chat_router
print("4")

from api.documents import router as document_router
print("5")

from api.auth import router as auth_router
print("6")

from api.workspaces import router as workspace_router
print("7")

from api.resume_analyzer import router as resume_router
print("8")

from api.interview import router as interview_router
print("9")

from api.resume_rewriter import router as resume_rewriter_router
print("10")


# from api.auth import router as auth_router
# from api.chat import router as chat_router
# from api.documents import router as document_router
# from api.interview import router as interview_router
# from api.resume_analyzer import router as resume_router
# from api.resume_rewriter import router as resume_rewriter_router
# from api.workspaces import router as workspace_router


from services.qdrant_service import create_collection

@asynccontextmanager
async def lifespan(app):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    try:
        create_collection()
    except Exception as e:
        print(f"Qdrant collection init skipped: {e}")

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