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
    is_active: bool = True

    last_run_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)