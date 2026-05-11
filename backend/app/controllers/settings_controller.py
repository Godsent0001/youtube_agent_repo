from fastapi import HTTPException

from app.services.agent_service import agent_service
from app.core.logger import logger


class SettingsController:
    """
    Controls AI agent behavior and configuration
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # GET SETTINGS
    # =========================
    def get_settings(self, agent_id: str):

        agent = agent_service.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        return {
            "agent_id": agent_id,
            "name": agent.get("name"),
            "niche": agent.get("niche"),
            "content_type": agent.get("content_type"),
            "custom_prompt": agent.get("custom_prompt"),
            "posting_frequency": agent.get("posting_frequency")
        }

    # =========================
    # UPDATE SETTINGS
    # =========================
    def update_settings(self, agent_id: str, payload: dict):

        updated = agent_service.update_agent(agent_id, payload)

        self.logger.info(f"Settings updated for agent {agent_id}")

        return {
            "message": "Settings updated successfully",
            "agent": updated
        }

    # =========================
    # RESET SETTINGS
    # =========================
    def reset_settings(self, agent_id: str):

        default_settings = {
            "custom_prompt": None,
            "posting_frequency": "daily",
            "content_type": "shorts"
        }

        updated = agent_service.update_agent(agent_id, default_settings)

        self.logger.info(f"Settings reset for agent {agent_id}")

        return {
            "message": "Agent reset to default AI settings",
            "agent": updated
        }


settings_controller = SettingsController()