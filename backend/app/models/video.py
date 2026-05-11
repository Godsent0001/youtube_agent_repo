from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict
from datetime import datetime


class Video(BaseModel):
    """
    AI Generated Video Model
    Represents a single output from the pipeline
    """

    # =========================
    # BASIC INFO
    # =========================
    id: Optional[str] = None

    user_id: str
    agent_id: str

    title: Optional[str] = None
    description: Optional[str] = None

    # =========================
    # CONTENT INFO
    # =========================
    content_type: Literal["shorts", "long"] = "shorts"

    topic: str
    niche: str

    script: str

    # =========================
    # MEDIA PIPELINE
    # =========================
    scenes: List[Dict] = Field(default_factory=list)
    media_sources: List[str] = Field(default_factory=list)

    audio_url: Optional[str] = None
    video_url: Optional[str] = None

    # =========================
    # YOUTUBE STATUS
    # =========================
    youtube_video_id: Optional[str] = None
    upload_status: Literal["pending", "processing", "uploaded", "failed"] = "pending"

    # =========================
    # PERFORMANCE METRICS (LIVE UPDATE)
    # =========================
    views: int = 0
    likes: int = 0
    comments: int = 0

    avg_watch_time: float = 0.0
    retention_rate: float = 0.0

    ctr: float = 0.0  # click-through rate (future ads)

    # =========================
    # SYSTEM DATA
    # =========================
    generation_time_seconds: float = 0.0

    error_log: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)