from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime


class User(BaseModel):
    """
    User model for authentication and subscription tracking
    """

    # =========================
    # CORE INFO
    # =========================
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None

    # =========================
    # SUBSCRIPTION INFO
    # =========================
    tier: Literal["free", "elite", "pro"] = "free"

    video_limit: int = 10
    videos_generated_this_month: int = 0

    stripe_customer_id: Optional[str] = None
    subscription_id: Optional[str] = None

    # =========================
    # SYSTEM DATA
    # =========================
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
