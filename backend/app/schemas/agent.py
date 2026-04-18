from pydantic import BaseModel
from typing import Optional, Literal


class AgentCreate(BaseModel):
    name: str
    niche: str

    content_type: Literal["shorts", "long"]

    custom_prompt: Optional[str] = None

    posting_frequency: Optional[Literal["daily", "weekly"]] = "daily"


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    niche: Optional[str] = None
    custom_prompt: Optional[str] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    niche: str
    content_type: str