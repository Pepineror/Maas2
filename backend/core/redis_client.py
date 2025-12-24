import redis
import json
from typing import Optional, Any
from backend.core.config import settings
from backend.core.logging import logger

class RedisClient:
    """
    Client for RealTimeCache (Redis).
    Handles caching of project metrics and evidence metadata.
    """
    def __init__(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            logger.info(f"Connected to Redis at {settings.REDIS_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        if not self.client: return None
        data = self.client.get(key)
        if data:
            try:
                return json.loads(data)
            except:
                return data
        return None

    def set(self, key: str, value: Any, expire_seconds: int = 3600):
        if not self.client: return
        try:
            val = json.dumps(value) if not isinstance(value, (str, bytes)) else value
            self.client.set(key, val, ex=expire_seconds)
        except Exception as e:
            logger.error(f"Redis SET failed for {key}: {e}")

    def delete(self, key: str):
        if self.client:
            self.client.delete(key)

# Singleton instance
redis_client = RedisClient()
