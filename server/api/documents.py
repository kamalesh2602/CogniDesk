from fastapi import APIRouter, UploadFile, File, Form
from db.mongo import db
from datetime import datetime
import os
import shutil
import uuid
from bson import ObjectId
from services.pdf_service import extract_pdf_text
from bson import ObjectId
from fastapi import HTTPException
from services.chuking_service import chunk_text
from services.pdf_service import extract_pdf_text
from services.document_chunk_service import store_chunks
from services.qdrant_service import client
from services.qdrant_service import create_collection
from services.embedding_service import generate_embedding
from services.vector_service import store_chunks_in_qdrant
from services.search_service import search_chunks
from services.chat_service import generate_answer
from services.search_service import get_context_chunks
from services.vector_service import delete_document_vectors

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    workspace_id: str = Form(...),
    file: UploadFile = File(...)
):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        upload_dir,
        unique_filename
    )

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
def get_workspace_documents(workspace_id: str):

    documents = []

    cursor = db.documents.find(
        {"workspace_id": workspace_id}
    ).sort("uploaded_at", -1)

    for document in cursor:

        document["_id"] = str(
            document["_id"]
        )

        documents.append(document)

    return documents

@router.get("/extract/{document_id}")
def extract_document_text(document_id: str):
    
    try:
        object_id = ObjectId(document_id)
        
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document id"
        )

    document = db.documents.find_one(
        {"_id": object_id}
    )

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
    
    text = extract_pdf_text(
        document["file_path"]
    )

    return {
        "document_id": document_id,
        "filename": document["filename"],
        "characters": len(text),
        "preview": text[:1000]
    }

@router.delete("/delete-collection")
def delete_collection():

    client.delete_collection(
        collection_name="document_chunks"
    )

    return {"message": "deleted"}


@router.delete("/{document_id}")
def delete_document(document_id: str):

    try:
        object_id = ObjectId(document_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document id"
        )

    document = db.documents.find_one(
        {"_id": object_id}
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if os.path.exists(document["file_path"]):
        os.remove(document["file_path"])

    db.document_chunks.delete_many(
        {
            "document_id": document_id
        }
    )
    delete_document_vectors(
    document_id
)
    db.documents.delete_one(
        {"_id": object_id}
    )

    return {
        "message": "Document deleted"
    }

    


@router.get("/chunks/{document_id}")
def get_document_chunks(document_id: str):

    try:
        object_id = ObjectId(document_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid document id"
        )

    document = db.documents.find_one(
        {"_id": object_id}
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_pdf_text(
        document["file_path"]
    )

    chunks = chunk_text(text)

    return {
        "document_id": document_id,
        "total_chunks": len(chunks),
        "first_chunk": chunks[0] if chunks else "",
        "last_chunk": chunks[-1] if chunks else ""
    }

@router.post("/process/{document_id}")
def process_document(
    document_id: str
):

    object_id = ObjectId(document_id)

    document = db.documents.find_one(
        {"_id": object_id}
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_pdf_text(
        document["file_path"]
    )

    chunks = chunk_text(text)

    count = store_chunks(
        document_id,
        document["workspace_id"],
        chunks
    )

    return {
        "chunks_created": count
    }

@router.get("/qdrant-test")
def qdrant_test():

    collections = client.get_collections()

    return collections.model_dump()

@router.post("/create-collection")
def create_qdrant_collection():

    result = create_collection()

    return {
        "status": result
    }




@router.get("/embedding-test")
def embedding_test():

    embedding = generate_embedding(
        "Hello World"
    )

    return {
        "dimension": len(embedding),
        "first_values": embedding[:5]
    }

@router.post("/embed/{document_id}")
def embed_document(document_id: str):

    chunks = list(
        db.document_chunks.find(
            {
                "document_id":
                    document_id
            }
        )
    )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No chunks found"
        )

    count = store_chunks_in_qdrant(
        chunks
    )

    return {
        "chunks_embedded": count
    }


@router.get("/collection-info")
def collection_info():

    return client.get_collection(
        "document_chunks"
    ).model_dump()

@router.get("/qdrant-version")
def qdrant_version():
    return {
        "methods": dir(client)
    }


@router.get("/search")
def test_search(query: str):

    results = search_chunks(query)

    return [
    {
        "score": point.score,
        "chunk_text": point.payload["chunk_text"]
    }
    for point in results.points
]

