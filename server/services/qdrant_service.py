from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance
)

client = QdrantClient(
    host="localhost",
    port=6333
)


def create_collection():

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if "document_chunks" not in existing:

        client.create_collection(
            collection_name="document_chunks",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        return "created"

    return "already exists"