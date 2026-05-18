from fastapi import APIRouter, HTTPException

from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job
from app.db.session import db
from datetime import datetime
import uuid
from app.services.video.video_service import video_service
from app.services.analytics.metrics_service import metrics_service

router = APIRouter(prefix="/videos", tags=["Videos"])


# =========================
# GET ALL VIDEOS (USER)
# =========================
@router.get("")
def get_user_videos(user_id: str):

    videos = video_service.get_user_videos(user_id)

    return videos


# =========================
# GET SINGLE VIDEO
# =========================
@router.get("/{video_id}")
def get_video(video_id: str):

    video = video_service.get_video(video_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    metrics = metrics_service.get_video_metrics(video_id)

    return {
        "video": video,
        "metrics": metrics
    }


# =========================
# REGENERATE VIDEO
# =========================
@router.post("/{video_id}/regenerate")
def regenerate_video(video_id: str):

    video = video_service.get_video(video_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if not video_queue:
        raise HTTPException(status_code=503, detail="Redis queue not available")

    video_job_id = str(uuid.uuid4())
    new_job = video_queue.enqueue(
        generate_video_job,
        agent_id=video["agent_id"],
        video_job_id=video_job_id
    )

    # Record in MongoDB using RQ job ID
    db["jobs"].insert_one({
        "job_id": new_job.id,
        "video_job_id": video_job_id,
        "user_id": video.get("user_id"),
        "agent_id": video["agent_id"],
        "status": "queued",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "result_url": None,
        "error": None
    })

    return {
        "message": "Video regeneration started",
        "video_id": video_id,
        "job_id": new_job.id
    }


# =========================
# RETRY FAILED VIDEO
# =========================
@router.post("/{video_id}/retry")
def retry_video(video_id: str):

    video = video_service.get_video(video_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.get("upload_status") != "failed":
        return {
            "message": "Video is not in failed state"
        }

    if not video_queue:
        raise HTTPException(status_code=503, detail="Redis queue not available")

    video_job_id = str(uuid.uuid4())
    new_job = video_queue.enqueue(
        generate_video_job,
        agent_id=video["agent_id"],
        video_job_id=video_job_id
    )

    # Record in MongoDB using RQ job ID
    db["jobs"].insert_one({
        "job_id": new_job.id,
        "video_job_id": video_job_id,
        "user_id": video.get("user_id"),
        "agent_id": video["agent_id"],
        "status": "queued",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "result_url": None,
        "error": None
    })

    return {
        "message": "Retry initiated",
        "video_id": video_id,
        "job_id": new_job.id
    }


# =========================
# DELETE VIDEO
# =========================
@router.delete("/{video_id}")
def delete_video(video_id: str):

    deleted = video_service.delete_video(video_id)

    return {
        "message": "Video deleted",
        "video_id": video_id
    }


# =========================
# VIDEO STATUS CHECK (PIPELINE TRACKING)
# =========================
@router.get("/{video_id}/status")
def video_status(video_id: str):

    video = video_service.get_video(video_id)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return {
        "video_id": video_id,
        "status": video.get("upload_status"),
        "current_stage": video.get("current_stage", "unknown")
    }