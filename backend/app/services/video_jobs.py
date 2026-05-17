from datetime import datetime, timedelta
import uuid
from app.services.pipeline_service import pipeline_service
from app.services.agent_service import agent_service
from app.db.session import db
from app.core.logger import logger

def update_job_status(job_id: str, status: str, result_url: str = None, error: str = None):
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

    db["jobs"].update_one({"job_id": job_id}, {"$set": update_data})

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

    # 1. Update status to processing
    update_job_status(job_id, "processing")

    try:
        # 2. Get agent
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise Exception(f"Agent {agent_id} not found")

        # 3. Run pipeline
        result = pipeline_service.run(agent)

        # 4. Update last run time
        agent_service.update_agent(agent_id, {"last_run_at": datetime.utcnow()})

        # 5. Update job as completed
        # Check result for youtube_upload and final_video_path
        res_url = None
        if isinstance(result, dict):
            res_url = result.get("final_video_path")

        update_job_status(job_id, "completed", result_url=res_url)
        logger.info(f"Job {job_id} completed successfully")

        # 6. Schedule NEXT run in 24 hours if agent is still active
        try:
            from app.queue.redis_queue import video_scheduler
            updated_agent = agent_service.get_agent(agent_id)
            if updated_agent and updated_agent.get("is_active", True) and video_scheduler:
                next_job_id = str(uuid.uuid4())

                # Create the job record for the future job
                db["jobs"].insert_one({
                    "job_id": next_job_id,
                    "user_id": updated_agent.get("user_id"),
                    "agent_id": agent_id,
                    "status": "queued",
                    "created_at": datetime.utcnow() + timedelta(hours=24),
                    "updated_at": datetime.utcnow(),
                    "result_url": None,
                    "error": None
                })

                video_scheduler.enqueue_in(
                    timedelta(hours=24),
                    generate_video_job,
                    agent_id=agent_id,
                    job_id=next_job_id
                )
                logger.info(f"Scheduled next run for agent {agent_id} in 24 hours (Job ID: {next_job_id})")
        except Exception as sched_err:
            logger.error(f"Failed to schedule next run: {sched_err}")

        return result

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        # 6. Update job as failed
        update_job_status(job_id, "failed", error=str(e))
        raise e
