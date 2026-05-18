from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class Agent(BaseModel):
    """
    AI YouTube Agent Model
    Represents an autonomous content creation system
    """

    # =========================
    # BASIC INFO
    # =========================
    id: Optional[str] = None
    user_id: str
    name: str = Field(..., description="Agent name (auto-generated or user-defined)")

    # =========================
    # CONTENT CONFIG
    # =========================
    niche: str = Field(..., description="Selected content niche")

    content_type: Literal["shorts", "long"] = "shorts"

    # AI determines topics automatically from niche
    auto_niche_intelligence: bool = True

    custom_prompt: Optional[str] = None

    # =========================
    # VIDEO SETTINGS
    # =========================
    video_length: Optional[int] = Field(
        default=None,
        description="Length in seconds (shorts) or minutes (long-form)"
    )

    posting_frequency: Literal["daily", "weekly"] = "daily"

    voice_style: Optional[str] = "energetic"

    subtitle_enabled: bool = True

    # =========================
    # MONETIZATION
    # =========================
    ads_enabled: bool = False
    selected_campaign_id: Optional[str] = None

    # =========================
    # LEARNING SYSTEM
    # =========================
    total_videos_created: int = 0

    avg_retention: float = 0.0

    best_performing_topics: List[str] = []

    worst_performing_topics: List[str] = []

    # =========================
    # STATUS
    # =========================
    is_active: bool = False

    status: Literal["idle", "queued", "processing"] = "idle"

    next_run_time: Optional[datetime] = Field(default_factory=datetime.utcnow)

    last_run_at: Optional[datetime] = None

    last_queued_at: Optional[datetime] = None

    # =========================
    # YOUTUBE OAUTH (AGENT LEVEL)
    # =========================
    youtube_access_token: Optional[str] = None
    youtube_refresh_token: Optional[str] = None
    youtube_token_expiry: Optional[datetime] = None
    youtube_channel_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)