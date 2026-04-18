from fastapi import HTTPException

from app.services.ads.ad_service import ad_service
from app.services.agent_service import agent_service
from app.core.logger import logger


class AdsController:
    """
    Controls all monetization logic
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # CREATE CAMPAIGN
    # =========================
    def create_campaign(self, payload: dict):

        campaign_id = ad_service.create_campaign(payload)

        self.logger.info(f"Campaign created: {campaign_id}")

        return campaign_id

    # =========================
    # ATTACH AD TO AGENT
    # =========================
    def attach_campaign(self, campaign_id: str, agent_id: str):

        agent = agent_service.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        result = ad_service.attach_to_agent(
            campaign_id=campaign_id,
            agent_id=agent_id
        )

        self.logger.info(f"Campaign {campaign_id} attached to agent {agent_id}")

        return result

    # =========================
    # GET CAMPAIGNS
    # =========================
    def get_agent_campaigns(self, agent_id: str):

        return ad_service.get_campaigns_by_agent(agent_id)

    # =========================
    # UPDATE CAMPAIGN STATUS
    # =========================
    def update_campaign_status(self, campaign_id: str, status: str):

        return ad_service.update_status(campaign_id, status)

    # =========================
    # INJECT AD INTO PIPELINE
    # =========================
    def inject_ad_context(self, agent_id: str):

        """
        This is VERY important:
        modifies script generation behavior
        """

        campaigns = ad_service.get_campaigns_by_agent(agent_id)

        if not campaigns:
            return None

        active_ads = [
            c for c in campaigns
            if c.get("status") == "active"
        ]

        return active_ads


ads_controller = AdsController()