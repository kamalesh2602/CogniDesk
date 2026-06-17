from fastapi import APIRouter
from models.chat import ChatRequest

from services.chat_service import generate_answer
from services.search_service import get_context_chunks
from services.chat_history_service import save_chat
from db.mongo import db
from bson import ObjectId

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
def ask_question(chat: ChatRequest):

    points = get_context_chunks(
        chat.question,
        chat.workspace_id
    )

    chunks = [
        point.payload["chunk_text"]
        for point in points
    ]

    sources = []

    for point in points:

        document = db.documents.find_one(
            {
                "_id": ObjectId(
                    point.payload["document_id"]
                )
            }
        )

    sources.append(
        {
            "filename":
                document["filename"]
                if document
                else "Unknown",

            "chunk_index":
                point.payload["chunk_index"],

            "score":
                round(point.score, 3)
        }
    )

    answer = generate_answer(
        chat.question,
        chunks
    )

    save_chat(
        chat.workspace_id,
        chat.question,
        answer
    )

    return {
        "question": chat.question,
        "answer": answer,
        "sources": sources
    }

@router.get("/history/{workspace_id}")
def get_chat_history(
    workspace_id: str
):

    chats = []

    cursor = db.chat_messages.find(
        {
            "workspace_id": workspace_id
        }
    ).sort("created_at", -1)

    for chat in cursor:

        chat["_id"] = str(chat["_id"])

        chats.append(chat)

    return chats