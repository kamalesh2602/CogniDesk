from fastapi import FastAPI

app = FastAPI()

print("MAIN STARTED")

from api.auth import router as auth_router
print("✓ auth")

from api.workspaces import router as workspace_router
print("✓ workspaces")

from api.documents import router as document_router
print("✓ documents")

app.include_router(auth_router)
app.include_router(workspace_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {"status": "OK"}