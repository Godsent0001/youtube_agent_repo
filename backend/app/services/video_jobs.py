from datetime import datetime
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
        update_job_status(job_id, "completed", result_url=result.get("video_url") if isinstance(result, dict) else None)
        logger.info(f"Job {job_id} completed successfully")

        return result

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        # 6. Update job as failed
        update_job_status(job_id, "failed", error=str(e))
        raise e
