import time
import queue
import threading

from app.core.logger import logger
from app.workers.tasks import task_service


class Worker:
    """
    Background worker that processes AI tasks
    """

    def __init__(self):
        self.logger = logger
        self.job_queue = queue.Queue()
        self.running = True

    # =========================
    # QUEUE MANAGEMENT
    # =========================

    def add_job(self, job_type: str, payload: dict):

        job = {
            "type": job_type,
            "payload": payload
        }

        self.job_queue.put(job)

        self.logger.info(f"Job added: {job_type}")

    # =========================
    # JOB PROCESSOR
    # =========================

    def process_job(self, job):

        job_type = job["type"]
        payload = job["payload"]

        try:
            if job_type == "generate_video":

                return task_service.generate_video_task(
                    agent_id=payload["agent_id"]
                )

            elif job_type == "retry_video":

                return task_service.retry_failed_video(payload)

            else:
                self.logger.warning(f"Unknown job type: {job_type}")

        except Exception as e:
            self.logger.error(f"Job failed: {e}")

            # optional retry logic
            self.job_queue.put({
                "type": "retry_video",
                "payload": payload
            })

    # =========================
    # WORKER LOOP
    # =========================

    def start(self):

        self.logger.info("Worker started...")

        while self.running:

            try:
                job = self.job_queue.get(timeout=5)

                self.logger.info(f"Processing job: {job['type']}")

                self.process_job(job)

            except queue.Empty:
                continue

            except Exception as e:
                self.logger.error(f"Worker error: {e}")

    # =========================
    # RUN IN BACKGROUND THREAD
    # =========================

    def start_background(self):

        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()

        self.logger.info("Worker running in background")

        return thread


worker = Worker()