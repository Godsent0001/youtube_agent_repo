import time
import uuid
from datetime import datetime
from app.db.session import db
from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job, on_video_job_failure
from app.core.logger import logger

class LoopScheduler:
    """
    Centralized MVP Loop Scheduler.
    Only ONE instance should run in the entire system.
    """

    def __init__(self, check_interval_seconds: int = 60):
        self.check_interval = check_interval_seconds

    def run(self):
        logger.info(f"Centralized Loop Scheduler started. Interval: {self.check_interval}s")

        while True:
            try:
                self.process_due_agents()
            except Exception as e:
                logger.error(f"Loop Scheduler Error: {e}")

            time.sleep(self.check_interval)

    def process_due_agents(self):
        # Automatic scheduling disabled as per user request.
        # Videos are now triggered manually via the "Generate Video" button.
        pass

    def enqueue_agent_job(self, agent):
        agent_id = str(agent["_id"])
        user_id = agent.get("user_id")

        # Generate our application-level tracking ID (which we also pass to RQ)
        custom_job_id = str(uuid.uuid4())

        logger.info(f"Scheduler: Enqueuing agent {agent_id} (Job ID: {custom_job_id})")

        try:
            # 2. Enqueue with POSITIONAL arguments to avoid keyword conflicts
            # rq_job = queue.enqueue(func, *args, **kwargs)
            # The second argument to enqueue is the first argument to our function
            new_job = video_queue.enqueue(
                generate_video_job,
                args=(agent_id, custom_job_id),
                job_timeout=3600,
                on_failure=on_video_job_failure
            )

            # 3. Create job record in MongoDB
            db["jobs"].insert_one({
                "job_id": custom_job_id, # We use our generated ID for tracking
                "rq_job_id": new_job.id, # Also store the internal RQ ID
                "user_id": user_id,
                "agent_id": agent_id,
                "status": "queued",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "result_url": None,
                "error": None
            })

            logger.info(f"Scheduler: Enqueued successfully. RQ ID: {new_job.id}")

        except Exception as e:
            logger.error(f"Scheduler: Failed to enqueue agent {agent_id}: {e}")
            # Reset agent status to idle if enqueuing fails so it can be picked up again
            from bson import ObjectId
            db["agents"].update_one(
                {"_id": ObjectId(agent_id)},
                {"$set": {"status": "idle"}}
            )

loop_scheduler = LoopScheduler()
