from fastapi import APIRouter, HTTPException

from app.workers.worker import worker
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

    worker.add_job("generate_video", {
        "agent_id": video["agent_id"]
    })

    return {
        "message": "Video regeneration started",
        "video_id": video_id
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

    worker.add_job("generate_video", {
        "agent_id": video["agent_id"]
    })

    return {
        "message": "Retry initiated",
        "video_id": video_id
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