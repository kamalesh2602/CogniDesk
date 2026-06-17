from services.embedding_service import generate_embedding
from services.qdrant_service import client
from qdrant_client.models import Filter
from qdrant_client.models import FieldCondition
from qdrant_client.models import MatchValue


def search_chunks(
    query,
    workspace_id,
    limit=3
):

    query_vector = generate_embedding(
        query
    )

    results = client.query_points(
        collection_name="document_chunks",

        query=query_vector,

        query_filter=Filter(
            must=[
                FieldCondition(
                    key="workspace_id",
                    match=MatchValue(
                        value=workspace_id
                    )
                )
            ]
        ),

        limit=limit
    )

    return results

def get_context_chunks(
    query,
    workspace_id
):

    results = search_chunks(
        query,
        workspace_id
    )

    chunks = []

    for point in results.points:

        chunks.append(
            point.payload["chunk_text"]
        )

    return  results.points
