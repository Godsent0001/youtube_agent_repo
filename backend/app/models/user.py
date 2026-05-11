from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class User(BaseModel):
    """
    Platform User Model
    Owns AI agents and campaigns
    """

    # =========================
    # BASIC INFO
    # =========================
    id: Optional[str] = None

    email: str
    username: str

    hashed_password: str

    full_name: Optional[str] = None

    # =========================
    # ACCOUNT TYPE
    # =========================
    plan: Literal["free", "pro", "enterprise"] = "free"

    is_active: bool = True
    is_verified: bool = False

    # =========================
    # RELATIONSHIPS
    # =========================
    agent_ids: List[str] = []
    campaign_ids: List[str] = []

    # =========================
    # STATS
    # =========================
    total_videos_created: int = 0
    total_views: int = 0

    # =========================
    # YOUTUBE OAUTH
    # =========================
    youtube_access_token: Optional[str] = None
    youtube_refresh_token: Optional[str] = None
    youtube_token_expiry: Optional[datetime] = None
    youtube_channel_id: Optional[str] = None

    # =========================
    # TIMESTAMPS
    # =========================
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None