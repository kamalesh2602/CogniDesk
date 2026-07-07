from threading import Lock

from core.config import settings

_model = None
_model_lock = Lock()


def get_model():
    """
    Lazily initialize the embedding model.

    The model is loaded only when the first embedding
    request is made, instead of during application startup.
    """

    global _model

    if _model is None:
        with _model_lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer

                _model = SentenceTransformer(
                    settings.EMBEDDING_MODEL
                )

    return _model


def generate_embedding(text: str) -> list[float]:
    """
    Generate embedding for the given text.
    """

    model = get_model()

    embedding = model.encode(text)

    return embedding.tolist()


def is_model_loaded() -> bool:
    """
    Returns whether the embedding model has already been loaded.
    """

    return _model is not None