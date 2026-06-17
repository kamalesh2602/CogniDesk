from db.mongo import db


def store_chunks(
    document_id,
    workspace_id,
    chunks
):

    chunk_documents = []

    for index, chunk in enumerate(chunks):

        chunk_documents.append({
            "document_id": document_id,
            "workspace_id": workspace_id,
            "chunk_index": index,
            "chunk_text": chunk
        })

    if chunk_documents:
        db.document_chunks.insert_many(
            chunk_documents
        )

    return len(chunk_documents)