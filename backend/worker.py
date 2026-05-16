import os
from rq import Worker, Queue, Connection
from app.queue.redis_queue import redis_conn

listen = ["video_generation"]

if __name__ == "__main__":
    if not redis_conn:
        print("REDIS_URL not set. Worker cannot start.")
        exit(1)

    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        print("Worker starting... listening on 'video_generation' queue.")
        worker.work()
