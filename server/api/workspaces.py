from fastapi import APIRouter, HTTPException
from models.workspace import WorkspaceCreate
from db.mongo import db
from datetime import datetime
from bson import ObjectId

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"]
)


def validate_object_id(workspace_id: str):
    try:
        return ObjectId(workspace_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid workspace id"
        )


def serialize_workspace(workspace):
    workspace["_id"] = str(workspace["_id"])
    return workspace


@router.post("/")
def create_workspace(workspace: WorkspaceCreate):

    data = {
        "name": workspace.name,
        "description": workspace.description,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = db.workspaces.insert_one(data)

    return {
        "id": str(result.inserted_id),
        "name": workspace.name,
        "description": workspace.description,
        "message": "Workspace created"
    }


@router.get("/")
def get_workspaces():

    workspaces = []

    cursor = db.workspaces.find().sort(
        "created_at",
        -1
    )

    for workspace in cursor:
        workspaces.append(
            serialize_workspace(workspace)
        )

    return workspaces


@router.get("/{workspace_id}")
def get_workspace(workspace_id: str):

    object_id = validate_object_id(workspace_id)

    workspace = db.workspaces.find_one(
        {"_id": object_id}
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return serialize_workspace(workspace)


@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: str,
    workspace: WorkspaceCreate
):

    object_id = validate_object_id(workspace_id)

    result = db.workspaces.update_one(
        {"_id": object_id},
        {
            "$set": {
                "name": workspace.name,
                "description": workspace.description,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    updated_workspace = db.workspaces.find_one(
        {"_id": object_id}
    )

    return serialize_workspace(updated_workspace)


@router.delete("/{workspace_id}")
def delete_workspace(workspace_id: str):

    object_id = validate_object_id(workspace_id)

    result = db.workspaces.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return {
        "message": "Workspace deleted"
    }