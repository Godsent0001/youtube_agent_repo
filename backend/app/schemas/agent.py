from pydantic import BaseModel
from typing import Optional, Literal


class AgentCreate(BaseModel):
    name: str
    niche: str

    content_type: Literal["shorts", "long"]

    custom_prompt: Optional[str] = None

    posting_frequency: Optional[Literal["daily", "weekly"]] = "daily"

    video_length: Optional[int] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    niche: Optional[str] = None
    custom_prompt: Optional[str] = None
    video_length: Optional[int] = None
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    niche: str
    content_type: str
    video_length: Optional[int] = None
    is_active: bool = True
    youtube_connected: bool = False