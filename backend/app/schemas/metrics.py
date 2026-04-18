from pydantic import BaseModel
from typing import Optional


class MetricsCreate(BaseModel):
    video_id: str
    agent_id: str

    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0

    avg_watch_time: float = 0.0
    retention_rate: float = 0.0
    ctr: float = 0.0


class MetricsResponse(BaseModel):
    video_id: str
    views: int
    retention_rate: float
    ctr: float