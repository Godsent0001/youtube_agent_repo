import os
import multiprocessing
import sys
import time

# Ensure current directory is in path
sys.path.append(os.getcwd())

from rq import Worker, Connection
from app.queue.redis_queue import redis_conn, video_queue

def run_worker():
    # Re-initialize for process safety
    from app.queue.redis_queue import redis_conn, video_queue
    print("Starting RQ Worker...")
    if not redis_conn:
        print("REDIS_URL not set. Worker cannot start.")
        return

    with Connection(redis_conn):
        # Use the pre-configured video_queue which has the 3600s default_timeout
        worker = Worker([video_queue])
        print(f"Worker listening on '{video_queue.name}' queue (Default Timeout: {video_queue.default_timeout}s)...")
        worker.work()

def run_scheduler_loop():
    # Re-import inside child process
    from app.services.loop_scheduler import loop_scheduler
    print("Starting Centralized Loop Scheduler Process...")
    try:
        loop_scheduler.run()
    except Exception as e:
        print(f"Loop Scheduler process failed: {e}")

if __name__ == "__main__":
    print("Worker Service entry point started...")

    # Log agent count for diagnosis
    try:
        from app.db.session import db
        count = db["agents"].count_documents({})
        print(f"DIAGNOSTIC: Found {count} agents in the database.")
    except Exception as e:
        print(f"DIAGNOSTIC ERROR: Could not count agents: {e}")

    if not redis_conn:
        print("REDIS_URL not set. Process cannot start.")
        sys.exit(1)

    # Use multiprocessing to run both the worker and the centralized scheduler
    # This keeps them in the same container but separate processes.

    worker_process = multiprocessing.Process(target=run_worker)
    scheduler_process = multiprocessing.Process(target=run_scheduler_loop)

    worker_process.start()
    scheduler_process.start()

    try:
        while True:
            # Monitor processes
            if not worker_process.is_alive():
                print("RQ Worker process died. Exiting container.")
                scheduler_process.terminate()
                sys.exit(1)

            if not scheduler_process.is_alive():
                print("Scheduler process died. Restarting...")
                scheduler_process = multiprocessing.Process(target=run_scheduler_loop)
                scheduler_process.start()

            time.sleep(15)
    except KeyboardInterrupt:
        print("Shutting down processes...")
        worker_process.terminate()
        scheduler_process.terminate()
