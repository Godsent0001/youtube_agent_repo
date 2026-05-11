import time
import queue
import threading

from app.core.logger import logger
from app.workers.tasks import task_service


class Worker:
    """
    Production-safe AI Worker System
    """

    def __init__(self):
        self.logger = logger
        self.job_queue = queue.Queue()
        self.running = True

        # 🔥 retry control
        self.max_retries = 3

    # =========================
    # ADD JOB
    # =========================
    def add_job(self, job_type: str, payload: dict):

        job = {
            "type": job_type,
            "payload": payload,
            "attempt": payload.get("attempt", 0),
            "created_at": time.time()
        }

        self.job_queue.put(job)

        self.logger.info(f"Job queued: {job_type}")

    # =========================
    # PROCESS JOB
    # =========================
    def process_job(self, job):

        job_type = job["type"]
        payload = job["payload"]
        attempt = job.get("attempt", 0)

        try:
            self.logger.info(
                f"Processing {job_type} (attempt {attempt})"
            )

            # =========================
            # ROUTING
            # =========================
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

            # =========================
            # SAFE RETRY LOGIC
            # =========================
            if attempt < self.max_retries:

                self.logger.info(
                    f"Retrying job (attempt {attempt + 1})"
                )

                time.sleep(2 ** attempt)  # exponential backoff

                payload["attempt"] = attempt + 1

                self.job_queue.put({
                    "type": job_type,
                    "payload": payload,
                    "attempt": attempt + 1
                })

            else:
                self.logger.error("Max retries reached. Job dropped.")

    # =========================
    # WORKER LOOP
    # =========================
    def start(self):

        self.logger.info("Worker started...")

        while self.running:

            try:
                job = self.job_queue.get(timeout=5)

                self.process_job(job)

            except queue.Empty:
                continue

            except Exception as e:
                self.logger.error(f"Worker loop error: {e}")

    # =========================
    # BACKGROUND THREAD
    # =========================
    def start_background(self):

        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()

        self.logger.info("Worker running in background")

        return thread


worker = Worker()