from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal
from datetime import datetime

class VideoBase(BaseModel):
    user_id: str
    agent_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Literal["shorts", "long"] = "shorts"
    topic: str
    niche: Optional[str] = ""
    script: str

class VideoCreate(VideoBase):
    pass

class VideoGenerateRequest(BaseModel):
    prompt: str
    content_type: Literal["shorts", "long"] = "shorts"
    video_length: int = 60

class VideoResponse(VideoBase):
    id: str
    scenes: List[Dict] = []
    media_sources: List[str] = []
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    status: str
    views: int
    likes: int
    comments: int
    created_at: datetime

    class Config:
        from_attributes = True

class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int
