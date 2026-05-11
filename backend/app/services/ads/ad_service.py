from bson import ObjectId
from app.db.session import campaigns_collection
from app.core.logger import logger

class AdService:
    """
    Service for managing Ad Campaigns.
    """
    def __init__(self):
        self.logger = logger

    def _prepare_campaign(self, campaign: dict):
        if campaign and "_id" in campaign:
            campaign["id"] = str(campaign.pop("_id"))
        return campaign

    def create_campaign(self, data: dict):
        """Create a new ad campaign."""
        result = campaigns_collection.insert_one(data)
        self.logger.info(f"Campaign created with ID: {result.inserted_id}")
        return str(result.inserted_id)

    def get_campaigns_by_agent(self, agent_id: str):
        """Retrieve all campaigns associated with a specific agent."""
        campaigns = list(campaigns_collection.find({"agent_id": agent_id}))
        return [self._prepare_campaign(c) for c in campaigns]

    def attach_to_agent(self, campaign_id: str, agent_id: str):
        """Attach an existing campaign to an agent."""
        try:
            result = campaigns_collection.update_one(
                {"_id": ObjectId(campaign_id)},
                {"$set": {"agent_id": agent_id}}
            )
            return result.modified_count > 0
        except Exception as e:
            self.logger.error(f"Error attaching campaign {campaign_id} to agent {agent_id}: {e}")
            return False

    def update_status(self, campaign_id: str, status: str):
        """Update the status of a campaign."""
        try:
            result = campaigns_collection.update_one(
                {"_id": ObjectId(campaign_id)},
                {"$set": {"status": status}}
            )
            return {"campaign_id": campaign_id, "status": status, "updated": result.modified_count > 0}
        except Exception as e:
            self.logger.error(f"Error updating campaign {campaign_id} status: {e}")
            raise

ad_service = AdService()
