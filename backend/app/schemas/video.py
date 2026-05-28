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
    audio_url: Optional[str] = None
    video_url: Optional[str] = None

    status: Optional[Literal["pending", "processing", "completed", "failed"]] = None


# =========================
# VIDEO RESPONSE (FRONTEND)
# =========================
class VideoResponse(BaseModel):
    id: str

    user_id: str
    agent_id: Optional[str] = None

    topic: str

    content_type: Literal["shorts", "long"]

    script: str

    video_url: Optional[str]

    status: Literal["pending", "processing", "completed", "failed"]

    views: int = 0
    likes: int = 0
    retention_rate: float = 0.0

    created_at: datetime