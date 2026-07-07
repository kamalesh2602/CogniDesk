from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType,
)

from core.config import settings


@lru_cache
def get_qdrant_client():
    kwargs = {
        "url": settings.QDRANT_URL,
        "check_compatibility": False,
    }

    if settings.QDRANT_API_KEY:
        kwargs["api_key"] = settings.QDRANT_API_KEY

    return QdrantClient(**kwargs)


def create_collection():
    client = get_qdrant_client()

    collections = client.get_collections()

    existing = [c.name for c in collections.collections]

    if "document_chunks" not in existing:

        client.create_collection(
            collection_name="document_chunks",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    # Create payload index (safe to call every startup)
    try:
        client.create_payload_index(
            collection_name="document_chunks",
            field_name="workspace_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
    except Exception:
        # Already exists
        pass

    return "ready"