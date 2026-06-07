from fastapi import APIRouter, HTTPException, Depends
from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job, on_video_job_failure
from app.db.session import db, videos_collection
from datetime import datetime
import uuid
from app.services.video.video_service import video_service
from app.schemas.video import VideoCreateRequest, VideoResponse
from typing import List, Optional

router = APIRouter(prefix="/videos", tags=["Videos"])


# =========================
# GET ALL VIDEOS (USER)
# =========================
@router.get("", response_model=List[VideoResponse])
def get_user_videos(user_id: Optional[str] = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    videos = video_service.get_user_videos(user_id)
    return videos


# =========================
# GET SINGLE VIDEO
# =========================
@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str):
    video = video_service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# =========================
# CREATE / GENERATE VIDEO
# =========================
@router.post("", status_code=201)
def create_video(request: VideoCreateRequest, user_id: Optional[str] = None):
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    if not video_queue:
        raise HTTPException(status_code=503, detail="Redis queue not available")

    # 1. Create Video Record
    video_data = {
        "user_id": user_id,
        "prompt": request.prompt,
        "aspect_ratio": request.aspect_ratio,
        "duration_seconds": request.duration_seconds,
        "status": "queued",
        "created_at": datetime.utcnow()
    }

    # If it's an edit
    if request.edit_prompt and request.original_video_id:
        video_data["edit_prompt"] = request.edit_prompt
        video_data["original_video_id"] = request.original_video_id

    video = video_service.create_video(video_data)
    video_id = video["id"]

    # 2. Enqueue Job
    custom_job_id = str(uuid.uuid4())
    new_job = video_queue.enqueue(
        generate_video_job,
        args=(video_id, custom_job_id),
        job_timeout=3600,
        on_failure=on_video_job_failure
    )

    # 3. Record Job in MongoDB
    db["jobs"].insert_one({
        "job_id": custom_job_id,
        "rq_job_id": new_job.id,
        "user_id": user_id,
        "video_id": video_id,
        "status": "queued",
        "progress": 0,
        "activities": [
            {"step": "Queued for processing", "timestamp": datetime.utcnow()}
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })

    return {
        "message": "Video generation started",
        "video_id": video_id,
        "job_id": custom_job_id
    }


# =========================
# DELETE VIDEO
# =========================
@router.delete("/{video_id}")
def delete_video(video_id: str):
    deleted = video_service.delete_video(video_id)
    if not deleted:
         raise HTTPException(status_code=404, detail="Video not found")
    return {
        "message": "Video deleted",
        "video_id": video_id
    }


# =========================
# VIDEO STATUS CHECK
# =========================
@router.get("/{video_id}/status")
def video_status(video_id: str):
    video = video_service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    # Find the latest job for this video
    job = db["jobs"].find_one({"video_id": video_id}, sort=[("created_at", -1)])

    return {
        "video_id": video_id,
        "status": video.get("status"),
        "progress": job.get("progress", 0) if job else 0,
        "activities": job.get("activities", []) if job else []
    }
