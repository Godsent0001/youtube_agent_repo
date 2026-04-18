import time
from app.core.logger import logger


class CacheService:
    """
    Simple in-memory cache for media results
    (upgrade later to Redis in production)
    """

    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
        self.logger = logger

    def set(self, key: str, value):
        self.cache[key] = {
            "data": value,
            "timestamp": time.time()
        }

    def get(self, key: str):
        item = self.cache.get(key)

        if not item:
            return None

        if time.time() - item["timestamp"] > self.ttl:
            del self.cache[key]
            return None

        return item["data"]

    def clear(self):
        self.cache = self.cache
        self.logger.info("Cache cleared")


cache_service = CacheService()