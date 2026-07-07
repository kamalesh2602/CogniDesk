from functools import lru_cache

from core.config import settings


@lru_cache
def get_openai_client():
    from openai import OpenAI

    return OpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )


@lru_cache
def get_tavily_client():
    from tavily import TavilyClient

    return TavilyClient(api_key=settings.TAVILY_API_KEY)


@lru_cache
def get_qdrant_client():
    from qdrant_client import QdrantClient

    kwargs = {
        "url": settings.QDRANT_URL,
        "check_compatibility": False,
    }

    if settings.QDRANT_API_KEY:
        kwargs["api_key"] = settings.QDRANT_API_KEY

    return QdrantClient(**kwargs)


@lru_cache
def get_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(settings.EMBEDDING_MODEL)
