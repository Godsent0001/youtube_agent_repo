from datetime import datetime
from bson import ObjectId
from app.core.logger import logger
from app.db.session import agents_collection as agent_collection


class AgentService:
    """
    Manages AI content agents
    Each agent is a self-contained content creator
    """

    def __init__(self):
        self.logger = logger

    def _prepare_agent(self, agent: dict):
        if agent and "_id" in agent:
            agent["id"] = str(agent.pop("_id"))
            # Add calculated field for schema
            agent["youtube_connected"] = bool(agent.get("youtube_refresh_token"))
        return agent

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
        agent = agent_collection.find_one({"_id": ObjectId(agent_id)})
        return self._prepare_agent(agent)

    def list_user_agents(self, user_id: str):
        agents = list(agent_collection.find({"user_id": user_id}))
        return [self._prepare_agent(a) for a in agents]

    def update_agent(self, agent_id: str, data: dict):
        """Update an existing agent."""
        try:
            agent_collection.update_one(
                {"_id": ObjectId(agent_id)},
                {"$set": data}
            )
            return self.get_agent(agent_id)
        except Exception as e:
            self.logger.error(f"Error updating agent {agent_id}: {e}")
            return None

    def delete_agent(self, agent_id: str):
        """Delete an agent by its ID."""
        try:
            result = agent_collection.delete_one({"_id": ObjectId(agent_id)})
            return result.deleted_count > 0
        except Exception as e:
            self.logger.error(f"Error deleting agent {agent_id}: {e}")
            return False


agent_service = AgentService()
