import time
import uuid
from datetime import datetime
from app.db.session import db
from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job
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
        now = datetime.utcnow()

        # Log periodic check
        if int(time.time()) % 300 < 60: # Log roughly once every 5 minutes to avoid noise
            logger.info(f"Scheduler: Checking for due agents at {now}. DB: {db.name}")

        # 1. Atomic check and update using find_one_and_update
        # Find one agent that is active, due for a run, and idle
        # Failed agents must be manually reset or retried to prevent infinite loops
        # Also handle cases where status or next_run_time might be missing
        agent = db["agents"].find_one_and_update(
            {
                "is_active": True,
                "status": {"$in": ["idle", None]},
                "$or": [
                    {"next_run_time": {"$lte": now}},
                    {"next_run_time": {"$exists": False}}
                ]
            },
            {
                "$set": {
                    "status": "queued",
                    "last_queued_at": now
                }
            },
            return_document=True
        )

        if agent:
            logger.info(f"Scheduler: Found due agent {agent.get('name')} ({agent.get('_id')}). Status: {agent.get('status')}. Next run was scheduled for {agent.get('next_run_time')}")
            self.enqueue_agent_job(agent)
            # Recursively check for more due agents without waiting the full interval
            # This allows processing multiple agents quickly if they are all due
            self.process_due_agents()

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
                agent_id,
                custom_job_id,
                job_timeout=3600
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
