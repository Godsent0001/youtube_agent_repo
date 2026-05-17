import os
import threading
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from rq import Worker, Queue, Connection
from app.queue.redis_queue import redis_conn, video_scheduler

listen = ["video_generation"]

def run_scheduler():
    if video_scheduler:
        print("Starting RQ Scheduler...")
        try:
            video_scheduler.run()
        except Exception as e:
            print(f"Scheduler failed: {e}")

if __name__ == "__main__":
    print("Worker entry point started...")

    if not redis_conn:
        print("REDIS_URL not set. Worker cannot start.")
        sys.exit(1)

    # Start scheduler in a separate thread within the same worker process
    # rq-scheduler is lightweight.
    print("Initializing components...")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        print("Worker listening on 'video_generation' queue...")
        worker.work()
