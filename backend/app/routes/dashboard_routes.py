from fastapi import APIRouter
from typing import Optional
from app.services.video.video_service import video_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================
# OVERALL USER DASHBOARD
# =========================
@router.get("/overview")
def get_overview(user_id: Optional[str] = None):
    if not user_id:
        return {"total_videos": 0, "recent_videos": []}
    videos = video_service.get_user_videos(user_id)
    return {
        "total_videos": len(videos),
        "recent_videos": videos[:5]
    }


# =========================
# VIDEO LIST
# =========================
@router.get("/videos")
def get_videos(user_id: Optional[str] = None):
    if not user_id:
        return []
    videos = video_service.get_user_videos(user_id)
    return videos


# =========================
# SINGLE VIDEO DETAILS
# =========================
@router.get("/videos/{video_id}")
def video_details(video_id: str):
    video = video_service.get_video(video_id)
    return {
        "video": video
    }
