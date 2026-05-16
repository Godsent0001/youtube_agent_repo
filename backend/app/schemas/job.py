from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobBase(BaseModel):
    job_id: str
    user_id: str
    agent_id: str
    status: str = "queued"
    created_at: datetime
    updated_at: datetime
    result_url: Optional[str] = None
    error: Optional[str] = None

class JobResponse(JobBase):
    pass
