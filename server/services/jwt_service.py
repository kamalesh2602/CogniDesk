from jose import jwt, JWTError
from datetime import datetime, timedelta

from core.config import settings


SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM


def create_access_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except JWTError:
        return None