from fastapi import HTTPException

from app.services.agent_service import agent_service
from app.workers.worker import worker
from app.core.logger import logger


class AgentController:
    """
    Controls AI agent lifecycle + execution
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # CREATE AGENT
    # =========================
    def create_agent(self, user_id: str, payload: dict):

        agent_id = agent_service.create_agent(user_id, payload)

        self.logger.info(f"Agent created: {agent_id}")

        return agent_id

    # =========================
    # GET AGENT
    # =========================
    def get_agent(self, agent_id: str):

        agent = agent_service.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        return agent

    # =========================
    # LIST USER AGENTS
    # =========================
    def list_agents(self, user_id: str):

        return agent_service.list_user_agents(user_id)

    # =========================
    # UPDATE AGENT SETTINGS
    # =========================
    def update_agent(self, agent_id: str, payload: dict):

        updated = agent_service.update_agent(agent_id, payload)

        self.logger.info(f"Agent updated: {agent_id}")

        return updated

    # =========================
    # DELETE AGENT
    # =========================
    def delete_agent(self, agent_id: str):

        result = agent_service.delete_agent(agent_id)

        self.logger.info(f"Agent deleted: {agent_id}")

        return result

    # =========================
    # TRIGGER VIDEO GENERATION
    # =========================
    def generate_video(self, agent_id: str):

        """
        Sends agent to worker queue
        """

        agent = agent_service.get_agent(agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        worker.add_job("generate_video", {
            "agent_id": agent_id
        })

        self.logger.info(f"Generation started for agent {agent_id}")

        return {
            "message": "Video generation started",
            "agent_id": agent_id
        }


agent_controller = AgentController()