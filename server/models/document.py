from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: str
    workspace_id: str
    filename: str
    file_path: str