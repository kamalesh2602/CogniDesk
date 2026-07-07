from qdrant_client.models import (
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)

from services.qdrant_service import get_qdrant_client
from services.embedding_service import generate_embedding


def store_chunks_in_qdrant(chunks):

    client = get_qdrant_client()

    points = []

    for chunk in chunks:

        embedding = generate_embedding(chunk["chunk_text"])

        points.append(
            PointStruct(
                id=abs(hash(str(chunk["_id"]))) % 1000000000000,
                vector=embedding,
                payload={
                    "document_id": chunk["document_id"],
                    "workspace_id": chunk["workspace_id"],
                    "filename": chunk["filename"],
                    "chunk_index": chunk["chunk_index"],
                    "chunk_text": chunk["chunk_text"],
                },
            )
        )

    client.upsert(
        collection_name="document_chunks",
        points=points,
    )

    return len(points)


def delete_document_vectors(document_id):

    client = get_qdrant_client()

    client.delete(
        collection_name="document_chunks",
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            )
        ),
    )