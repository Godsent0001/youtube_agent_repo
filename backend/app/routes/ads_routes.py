from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.campaign import CampaignCreate, CampaignResponse
from app.services.ads.ad_service import ad_service

router = APIRouter(prefix="/ads", tags=["Ads & Monetization"])


# =========================
# CREATE AD CAMPAIGN
# =========================
@router.post("/", response_model=str)
def create_campaign(payload: CampaignCreate):

    campaign_id = ad_service.create_campaign(payload.dict())

    return campaign_id


# =========================
# GET ALL CAMPAIGNS FOR AGENT
# =========================
@router.get("/agent/{agent_id}", response_model=List[dict])
def get_agent_campaigns(agent_id: str):

    return ad_service.get_campaigns_by_agent(agent_id)


# =========================
# ATTACH AD TO VIDEO PIPELINE
# =========================
@router.post("/{campaign_id}/attach")
def attach_campaign_to_pipeline(campaign_id: str, agent_id: str):

    result = ad_service.attach_to_agent(
        campaign_id=campaign_id,
        agent_id=agent_id
    )

    return {
        "message": "Campaign attached successfully",
        "result": result
    }


# =========================
# UPDATE CAMPAIGN STATUS
# =========================
@router.put("/{campaign_id}/status")
def update_status(campaign_id: str, status: str):

    return ad_service.update_status(campaign_id, status)