from datetime import datetime
from bson import ObjectId
from app.core.logger import logger
from app.db.session import agent_collection


class AgentService:
    """
    Manages AI content agents
    Each agent is a self-contained content creator
    """

    def __init__(self):
        self.logger = logger

    def create_agent(self, user_id: str, data: dict):

        agent = {
            "user_id": user_id,
            "name": data.get("name"),
            "niche": data.get("niche"),
            "content_type": data.get("content_type", "shorts"),

            "custom_prompt": data.get("custom_prompt", None),

            "posting_frequency": data.get("posting_frequency", "daily"),

            "created_at": datetime.utcnow(),

            "stats": {
                "videos_created": 0,
                "total_views": 0
            }
        }

        result = agent_collection.insert_one(agent)

        self.logger.info(f"Agent created: {result.inserted_id}")

        return str(result.inserted_id)

    def get_agent(self, agent_id: str):
        return agent_collection.find_one({"_id": ObjectId(agent_id)})

    def list_user_agents(self, user_id: str):
        return list(agent_collection.find({"user_id": user_id}))


agent_service = AgentService()