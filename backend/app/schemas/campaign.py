from pydantic import BaseModel
from typing import Optional, Literal


class CampaignCreate(BaseModel):
    agent_id: str

    ad_type: Literal["affiliate", "sponsored"]

    product_name: Optional[str] = None
    product_url: Optional[str] = None

    instruction: Optional[str] = None  # how AI should integrate ad


class CampaignResponse(BaseModel):
    id: str
    agent_id: str
    ad_type: str
    status: Literal["active", "paused", "completed"]