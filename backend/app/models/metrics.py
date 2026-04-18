from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal
from datetime import datetime


class Metrics(BaseModel):
    """
    Performance Metrics Model
    Used for AI learning and optimization
    """

    # =========================
    # IDENTIFIERS
    # =========================
    id: Optional[str] = None

    user_id: str
    agent_id: str
    video_id: str

    # =========================
    # CORE PERFORMANCE
    # =========================
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0

    # =========================
    # RETENTION ANALYTICS
    # =========================
    avg_watch_time: float = 0.0
    retention_rate: float = 0.0

    first_3_sec_retention: float = 0.0
    drop_off_rate: float = 0.0

    # =========================
    # MONETIZATION
    # =========================
    estimated_revenue: float = 0.0
    ad_clicks: int = 0
    ctr: float = 0.0

    # =========================
    # AI LEARNING SIGNALS
    # =========================
    topic_score: float = 0.0
    hook_score: float = 0.0
    script_score: float = 0.0

    performance_label: Literal["viral", "good", "average", "bad"] = "average"

    # =========================
    # SYSTEM INFO
    # =========================
    collected_at: datetime = Field(default_factory=datetime.utcnow)