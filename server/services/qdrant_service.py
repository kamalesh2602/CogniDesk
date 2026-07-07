from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from core.config import settings


from functools import lru_cache

@lru_cache
def get_qdrant_client():
    kwargs = {
        "url": settings.QDRANT_URL,
    }

    if settings.QDRANT_API_KEY:
        kwargs["api_key"] = settings.QDRANT_API_KEY

    return QdrantClient(**kwargs)


client = get_qdrant_client()



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
                distance=Distance.COSINE,
            ),
        )

        return "created"

    return "already exists"