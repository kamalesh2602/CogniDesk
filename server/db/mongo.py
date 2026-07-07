from functools import lru_cache

from pymongo import MongoClient
from core.config import settings


@lru_cache
def get_db_client():
    return MongoClient(settings.MONGO_URI)


class LazyDatabase:
    def __getattr__(self, item):
        return getattr(get_db_client()[settings.DATABASE_NAME], item)

    def __getitem__(self, item):
        return get_db_client()[settings.DATABASE_NAME][item]


db = LazyDatabase()
