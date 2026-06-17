from pydantic import BaseModel
from datetime import datetime

class WorkspaceCreate(BaseModel):
    name: str
    description: str = ""

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime