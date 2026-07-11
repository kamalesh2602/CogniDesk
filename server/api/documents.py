import os
import shutil
import uuid
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse

from db.mongo import db
from services.current_user import get_current_user
from services.pdf_service import extract_pdf_text
from services.chuking_service import chunk_text
from services.document_chunk_service import store_chunks
from services.embedding_service import generate_embedding
from services.qdrant_service import (
    get_qdrant_client,
    create_collection
)
# from services.embedding_service import generate_embedding
from services.vector_service import store_chunks_in_qdrant, delete_document_vectors
from services.search_service import search_chunks
from services.summary_service import generate_summary
from services.suggestion_service import generate_questions
from core.config import settings

UPLOAD_DIR = settings.UPLOAD_DIR


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    workspace_id: str = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    workspace = db.workspaces.find_one({
        "_id": ObjectId(workspace_id),
        "user_id": str(current_user["_id"])
    })

    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata
    document = {
        "workspace_id": workspace_id,
        "filename": file.filename,
        "stored_filename": unique_filename,
        "file_path": file_path,
        "uploaded_at": datetime.utcnow()
    }

    result = db.documents.insert_one(document)

    return {
        "id": str(result.inserted_id),
        "workspace_id": workspace_id,
        "filename": file.filename,
        "stored_filename": unique_filename,
        "file_path": file_path,
        "message": "Document uploaded successfully"
    }


@router.get("/workspace/{workspace_id}")
def get_workspace_documents(
    workspace_id: str,
    current_user=Depends(get_current_user)
):
    workspace = db.workspaces.find_one({
        "_id": ObjectId(workspace_id),
        "user_id": str(current_user["_id"])
    })

    if not workspace:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    documents = []

    cursor = db.documents.find(
        {
            "workspace_id": workspace_id
        }
    ).sort(
        "uploaded_at",
        -1
    )

    for document in cursor:

        # Auto-clean orphaned records
        if not os.path.exists(document["file_path"]):

            db.document_chunks.delete_many(
                {
                    "document_id": str(document["_id"])
                }
            )

            try:
                delete_document_vectors(
                    str(document["_id"])
                )
            except Exception:
                pass

            db.documents.delete_one(
                {
                    "_id": document["_id"]
                }
            )

            continue

        document["_id"] = str(document["_id"])
        documents.append(document)

    return documents


@router.get("/extract/{document_id}")
def extract_document_text(document_id: str):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    if not os.path.exists(document["file_path"]):
        raise HTTPException(
            status_code=404, 
            detail="Physical file not found"
        )
    
    text = extract_pdf_text(document["file_path"])

    return {
        "document_id": document_id,
        "filename": document["filename"],
        "characters": len(text),
        "preview": text[:1000]
    }


@router.delete("/delete-collection")
def delete_collection():
    get_qdrant_client().delete_collection(collection_name="document_chunks")
    return {"message": "deleted"}


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    workspace = db.workspaces.find_one({
        "_id": ObjectId(document["workspace_id"]),
        "user_id": str(current_user["_id"])
    })
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    if os.path.exists(document["file_path"]):
        os.remove(document["file_path"])

    db.document_chunks.delete_many({"document_id": document_id})
    delete_document_vectors(document_id)
    db.documents.delete_one({"_id": object_id})

    return {"message": "Document deleted"}


@router.get("/chunks/{document_id}")
def get_document_chunks(document_id: str):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    text = extract_pdf_text(document["file_path"])
    chunks = chunk_text(text)

    return {
        "document_id": document_id,
        "total_chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else "",
        "last_chunk": chunks[-1] if chunks else ""
    }


@router.post("/process/{document_id}")
def process_document(
    document_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    workspace = db.workspaces.find_one({
        "_id": ObjectId(document["workspace_id"]),
        "user_id": str(current_user["_id"])
    })
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    text = extract_pdf_text(document["file_path"])
    chunks = chunk_text(text)
    
    count = store_chunks(
        document_id,
        document["workspace_id"],
        document["filename"],
        chunks
    )

    return {"chunks_created": count}


@router.get("/qdrant-test")
def qdrant_test():
    collections = get_qdrant_client().get_collections()
    return collections.model_dump()


@router.post("/create-collection")
def create_qdrant_collection():
    result = create_collection()
    return {"status": result}


@router.get("/embedding-test")
def embedding_test():
    embedding = generate_embedding("Hello World")
    return {
        "dimension": len(embedding),
        "first_values": embedding[:5]
    }


@router.post("/embed/{document_id}")
def embed_document(
    document_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    workspace = db.workspaces.find_one({
        "_id": ObjectId(document["workspace_id"]),
        "user_id": str(current_user["_id"])
    })
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    chunks = list(db.document_chunks.find({"document_id": document_id}))
    if not chunks:
        raise HTTPException(
            status_code=404, 
            detail="No chunks found"
        )

    count = store_chunks_in_qdrant(chunks)

    return {"chunks_embedded": count}


@router.get("/collection-info")
def collection_info():
    return get_qdrant_client().get_collection("document_chunks").model_dump()


@router.get("/qdrant-version")
def qdrant_version():
    return {
    "methods": dir(get_qdrant_client())
}


@router.get("/search")
def test_search(query: str, workspace_id: str):
    results = search_chunks(query, workspace_id)
    return [
        {
            "score": point.score,
            "chunk_text": point.payload["chunk_text"]
        }
        for point in results.points
    ]


@router.post("/summary/{document_id}")
def create_summary(
    document_id: str,
    current_user=Depends(get_current_user)
):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    workspace = db.workspaces.find_one({
        "_id": ObjectId(document["workspace_id"]),
        "user_id": str(current_user["_id"])
    })
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    text = extract_pdf_text(document["file_path"])
    text = text[:settings.SUMMARY_MAX_CHARS]
    
    summary = generate_summary(text)
    questions = generate_questions(text)

    db.documents.update_one(
        {"_id": object_id},
        {
            "$set": {
                "summary": summary,
                "suggested_questions": questions
            }
        }
    )

    return {"summary": summary}


@router.get("/view/{document_id}")
def view_document(
    document_id: str
):
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400, 
            detail="Invalid document id"
        )

    document = db.documents.find_one({"_id": object_id})
    if not document:
        raise HTTPException(
            status_code=404, 
            detail="Document not found"
        )

    workspace = db.workspaces.find_one({
        "_id": ObjectId(document["workspace_id"])
        # "user_id": str(current_user["_id"])
    })
    if not workspace:
        raise HTTPException(
            status_code=403, 
            detail="Access denied"
        )

    if not os.path.exists(document["file_path"]):
        raise HTTPException(
            status_code=404, 
            detail="Physical file not found"
        )

    return FileResponse(
        document["file_path"],
        media_type="application/pdf",
        filename=document["filename"] #comment this to avoid downloading 
    )