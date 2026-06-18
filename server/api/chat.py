from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from bson import ObjectId

from models.chat import ChatRequest

from services.chat_service import generate_answer
from services.search_service import get_context_chunks
from services.chat_history_service import save_chat
from services.current_user import get_current_user

from db.mongo import db
from services.research_agent import research

from services.writer_agent import  write_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask")
def ask_question(
    chat: ChatRequest,
    current_user=Depends(get_current_user)
):

    workspace = db.workspaces.find_one(
        {
            "_id": ObjectId(
                chat.workspace_id
            ),
            "user_id": str(
                current_user["_id"]
            )
        }
    )

    if not workspace:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    notes = research(
    chat.question,
    chat.workspace_id
)

    answer = write_answer(
        chat.question,
        notes
    )

    sources = []

# workspace files
    for filename in set(
        notes["workspace_sources"]
    ):
        sources.append(
            {
                "type": "document",
                "filename": filename
            }
        )

    # web sources
    for source in notes["sources"]:
        sources.append(
            {
                "type": "web",
                "title": source["title"],
                "url": source["url"]
            }
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
    workspace_id: str,
    current_user=Depends(get_current_user)
):

    workspace = db.workspaces.find_one(
        {
            "_id": ObjectId(
                workspace_id
            ),
            "user_id": str(
                current_user["_id"]
            )
        }
    )

    if not workspace:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    chats = []

    cursor = db.chat_messages.find(
        {
            "workspace_id": workspace_id
        }
    ).sort(
        "created_at",
        -1
    )

    for chat in cursor:

        chat["_id"] = str(
            chat["_id"]
        )

        chats.append(chat)

    return chats

@router.delete("/history/{workspace_id}")
def clear_chat_history(
    workspace_id: str,
    current_user=Depends(get_current_user)
):

    workspace = db.workspaces.find_one(
        {
            "_id": ObjectId(workspace_id),
            "user_id": str(
                current_user["_id"]
            )
        }
    )

    if not workspace:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    db.chat_messages.delete_many(
        {
            "workspace_id": workspace_id
        }
    )

    return {
        "message":
        "Chat history cleared"
    }


from services.tavily_service import search_web

@router.get("/web-search")
def web_search_test(
    query: str
):

    results = search_web(
        query
    )

    return results