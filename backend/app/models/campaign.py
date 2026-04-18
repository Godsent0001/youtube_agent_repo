from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class Campaign(BaseModel):
    """
    Monetization Campaign Model
    Injects ads into AI-generated videos
    """

    # =========================
    # BASIC INFO
    # =========================
    id: Optional[str] = None
    user_id: str

    name: str = Field(..., description="Campaign name")

    # =========================
    # AD CONFIG
    # =========================
    type: Literal["affiliate", "brand", "sponsored"] = "affiliate"

    product_name: Optional[str] = None

    product_url: Optional[str] = None

    call_to_action: Optional[str] = "Check this out"

    # =========================
    # TARGETING
    # =========================
    niches: List[str] = Field(
        default_factory=list,
        description="Niches this campaign applies to"
    )

    target_agent_ids: List[str] = []

    # =========================
    # PERFORMANCE TRACKING
    # =========================
    total_clicks: int = 0

    total_views: int = 0

    conversion_rate: float = 0.0

    revenue_generated: float = 0.0

    # =========================
    # SETTINGS
    # =========================
    is_active: bool = True

    priority_weight: int = 1  # used for ad selection

    created_at: datetime = Field(default_factory=datetime.utcnow)