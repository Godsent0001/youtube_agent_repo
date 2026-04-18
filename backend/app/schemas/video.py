from pydantic import BaseModel
from typing import Optional, List, Literal, Dict
from datetime import datetime


# =========================
# CREATE VIDEO (INTERNAL PIPELINE INPUT)
# =========================
class VideoCreate(BaseModel):
    agent_id: str
    user_id: str

    topic: str
    niche: str

    content_type: Literal["shorts", "long"]

    script: str

    scenes: Optional[List[Dict]] = []
    media_sources: Optional[List[str]] = []


# =========================
# UPDATE VIDEO (PIPELINE PROGRESS)
# =========================
class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    audio_url: Optional[str] = None
    video_url: Optional[str] = None

    upload_status: Optional[Literal["pending", "processing", "uploaded", "failed"]] = None


# =========================
# YOUTUBE UPLOAD RESULT
# =========================
class VideoUploadResponse(BaseModel):
    video_id: str
    youtube_url: str
    upload_status: Literal["uploaded", "failed"]


# =========================
# VIDEO RESPONSE (FRONTEND)
# =========================
class VideoResponse(BaseModel):
    id: str

    user_id: str
    agent_id: str

    title: Optional[str]
    description: Optional[str]

    topic: str
    niche: str

    content_type: Literal["shorts", "long"]

    script: str

    video_url: Optional[str]
    thumbnail_url: Optional[str]

    upload_status: Literal["pending", "processing", "uploaded", "failed"]

    views: int = 0
    likes: int = 0
    retention_rate: float = 0.0

    created_at: datetime