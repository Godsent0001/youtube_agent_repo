from pydantic import BaseModel
from typing import Optional, List, Literal, Dict
from datetime import datetime


# =========================
# CREATE VIDEO
# =========================
class VideoCreateRequest(BaseModel):
    prompt: str
    aspect_ratio: Literal["16:9", "9:16"] = "16:9"
    duration_seconds: int = 30
    edit_prompt: Optional[str] = None
    original_video_id: Optional[str] = None


class VideoCreate(BaseModel):
    user_id: str
    prompt: str
    aspect_ratio: Literal["16:9", "9:16"] = "16:9"
    duration_seconds: int = 30


# =========================
# UPDATE VIDEO
# =========================
class VideoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    status: Optional[Literal["queued", "processing", "completed", "failed"]] = None
    error_log: Optional[str] = None


# =========================
# VIDEO RESPONSE (FRONTEND)
# =========================
class VideoResponse(BaseModel):
    id: str
    user_id: str

    title: Optional[str]
    description: Optional[str]

    prompt: str
    aspect_ratio: Literal["16:9", "9:16"]
    duration_seconds: int

    script: Optional[str]
    video_url: Optional[str]
    thumbnail_url: Optional[str]

    status: Literal["queued", "processing", "completed", "failed"]

    created_at: datetime
