import os
import redis
from rq import Queue

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    # In local dev/debug mode without Redis, we might want a fallback or just fail early
    # For now, we'll assume it's provided in production as per requirements
    redis_conn = None
    video_queue = None
else:
    redis_conn = redis.from_url(REDIS_URL)
    video_queue = Queue("video_generation", connection=redis_conn)
