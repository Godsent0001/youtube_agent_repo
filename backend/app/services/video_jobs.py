from datetime import datetime, timedelta
import uuid
from rq import get_current_job
from app.services.pipeline_service import pipeline_service
from app.services.agent_service import agent_service
from app.db.session import db
from app.core.logger import logger
from bson import ObjectId

def update_job_status(job_id: str, status: str, result_url: str = None, error: str = None, progress: int = None):
    """
    Helper to update job status in MongoDB
    """
    update_data = {
        "status": status,
        "updated_at": datetime.utcnow()
    }
    if result_url:
        update_data["result_url"] = result_url
    if error:
        update_data["error"] = error
    if progress is not None:
        update_data["progress"] = progress

    db["jobs"].update_one({"job_id": job_id}, {"$set": update_data})

def update_job_activity(job_id: str, activity: str, progress: int = None):
    """
    Append a granular activity log to the job record
    """
    update_ops = {
        "$push": {
            "activities": {
                "step": activity,
                "timestamp": datetime.utcnow()
            }
        },
        "$set": {"updated_at": datetime.utcnow()}
    }

    if progress is not None:
        update_ops["$set"]["progress"] = progress

    db["jobs"].update_one({"job_id": job_id}, update_ops)

def generate_video_job(agent_id: str, job_id: str):
    """
    Background job to run the full video generation pipeline
    """
    logger.info(f"Starting video generation job {job_id} for agent {agent_id}")

    # Ensure storage directories exist in the worker environment
    import os
    os.makedirs("storage/audio", exist_ok=True)
    os.makedirs("storage/images", exist_ok=True)
    os.makedirs("storage/videos", exist_ok=True)

    # 1. Update job status to processing
    update_job_status(job_id, "processing")

    # 2. Update agent status to processing
    db["agents"].update_one(
        {"_id": ObjectId(agent_id)},
        {"$set": {"status": "processing"}}
    )

    try:
        # 3. Get agent
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise Exception(f"Agent {agent_id} not found")

        # 4. Run pipeline
        result = pipeline_service.run(agent, job_id)

        # 5. Update agent stats and next run
        now = datetime.utcnow()
        db["agents"].update_one(
            {"_id": ObjectId(agent_id)},
            {
                "$set": {
                    "status": "idle",
                    "last_run_at": now,
                    "next_run_time": now + timedelta(hours=24)
                }
            }
        )

        # 6. Update job as completed
        res_url = None
        if isinstance(result, dict):
            res_url = result.get("final_video_path")

        update_job_status(job_id, "completed", result_url=res_url)
        logger.info(f"Job {job_id} completed successfully")

        return result

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")

        # Mark agent as failed but keep is_active as is
        db["agents"].update_one(
            {"_id": ObjectId(agent_id)},
            {"$set": {"status": "failed"}}
        )

        # Update job as failed
        update_job_status(job_id, "failed", error=str(e))
        raise e
