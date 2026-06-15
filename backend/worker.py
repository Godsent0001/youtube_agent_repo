import os
import sys
import time
from rq import Worker, Connection

# Ensure current directory is in path
sys.path.append(os.getcwd())

def run_worker():
    # Re-initialize for process safety
    from app.queue.redis_queue import redis_conn, video_queue
    from app.core.config import settings

    print("========================================")
    print("Starting MorphFlow RQ Worker...")
    print(f"BACKEND_URL: {settings.BACKEND_URL}")
    print(f"REDIS_URL: {settings.REDIS_URL}")
    print("========================================")

    if not redis_conn:
        print("REDIS_URL not set. Worker cannot start.")
        return

    with Connection(redis_conn):
        worker = Worker([video_queue])
        print(f"Worker listening on '{video_queue.name}' queue...")
        worker.work()

if __name__ == "__main__":
    run_worker()
