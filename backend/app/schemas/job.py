from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ActivityStep(BaseModel):
    step: str
    timestamp: datetime

class JobBase(BaseModel):
    job_id: str
    user_id: str
    video_id: str
    status: str = "queued"
    progress: int = 0
    created_at: datetime
    updated_at: datetime
    result_url: Optional[str] = None
    error: Optional[str] = None
    activities: List[ActivityStep] = []

class JobResponse(JobBase):
    id: str
