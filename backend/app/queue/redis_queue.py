import os
import redis
from rq import Queue
from rq_scheduler import Scheduler

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    # In local dev/debug mode without Redis, we might want a fallback or just fail early
    # For now, we'll assume it's provided in production as per requirements
    redis_conn = None
    video_queue = None
    video_scheduler = None
else:
    redis_conn = redis.from_url(REDIS_URL)
    # Set default_timeout to 1 hour (3600s) to ensure long rendering jobs don't time out
    video_queue = Queue("video_generation", connection=redis_conn, default_timeout=3600)
    video_scheduler = Scheduler(queue=video_queue, connection=redis_conn)
