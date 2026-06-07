from datetime import datetime, timedelta
import uuid
import rq
from app.services.pipeline_service import pipeline_service
from app.services.video.video_service import video_service
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

def on_video_job_failure(job, connection, type, value, traceback):
    """
    Failure callback for RQ jobs
    """
    try:
        video_id = job.args[0]
        custom_job_id = job.args[1]
        logger.error(f"RQ Failure Callback: Job {custom_job_id} failed for video {video_id}. Error: {value}")

        from app.db.session import db, videos_collection
        from bson import ObjectId

        # Mark video as failed
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"status": "failed", "error_log": str(value)}}
        )

        # Mark job as failed
        db["jobs"].update_one(
            {"job_id": custom_job_id},
            {"$set": {
                "status": "failed",
                "error": f"RQ System Error: {str(value)}",
                "updated_at": datetime.utcnow()
            }}
        )
    except Exception as e:
        logger.error(f"Error in on_video_job_failure: {e}")

def generate_video_job(video_id: str, job_id: str):
    """
    Background job to run the full video generation pipeline
    """
    # Diagnostic: log current timeout
    current_job = rq.get_current_job()
    timeout = current_job.timeout if current_job else "unknown"
    logger.info(f"Starting video generation job {job_id} for video {video_id}. Timeout: {timeout}s")

    # Ensure storage directories exist in the worker environment
    import os
    os.makedirs("storage/audio", exist_ok=True)
    os.makedirs("storage/images", exist_ok=True)
    os.makedirs("storage/videos", exist_ok=True)

    # 1. Update job status to processing
    update_job_status(job_id, "processing")

    # 2. Update video status to processing
    from app.db.session import videos_collection
    videos_collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"status": "processing"}}
    )

    try:
        # 3. Get video record
        video = video_service.get_video(video_id)
        if not video:
            raise Exception(f"Video {video_id} not found")

        # 4. Run pipeline
        result = pipeline_service.run(video, job_id)

        # 5. Update video status
        res_url = None
        if isinstance(result, dict):
            res_url = result.get("final_video_path")

        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {
                "status": "completed",
                "video_url": res_url,
                "thumbnail_url": result.get("thumbnail_url") if isinstance(result, dict) else None
            }}
        )

        # 6. Update job as completed
        update_job_status(job_id, "completed", result_url=res_url)
        logger.info(f"Job {job_id} completed successfully")

        return result

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")

        # Mark video as failed
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"status": "failed", "error_log": str(e)}}
        )

        # Update job as failed
        update_job_status(job_id, "failed", error=str(e))
        raise e
