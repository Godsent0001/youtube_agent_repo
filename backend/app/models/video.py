from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict
from datetime import datetime


class Video(BaseModel):
    """
    AI Generated Video Model (MorphFlow)
    Represents a single output from the pipeline
    """

    # =========================
    # BASIC INFO
    # =========================
    id: Optional[str] = None
    user_id: str

    title: Optional[str] = None
    description: Optional[str] = None

    # =========================
    # CONTENT INFO
    # =========================
    aspect_ratio: Literal["16:9", "9:16"] = "16:9"
    duration_seconds: int = 30
    prompt: str

    script: Optional[str] = None

    # =========================
    # MEDIA PIPELINE
    # =========================
    scenes: List[Dict] = Field(default_factory=list)
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None # Keep for preview list

    # =========================
    # SYSTEM DATA
    # =========================
    status: Literal["queued", "processing", "completed", "failed"] = "queued"
    generation_time_seconds: float = 0.0
    error_log: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
