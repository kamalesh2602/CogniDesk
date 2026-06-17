from db.mongo import db
from datetime import datetime


def save_chat(
    workspace_id,
    question,
    answer
):

    db.chat_messages.insert_one(
        {
            "workspace_id": workspace_id,
            "question": question,
            "answer": answer,
            "created_at": datetime.utcnow()
        }
    )