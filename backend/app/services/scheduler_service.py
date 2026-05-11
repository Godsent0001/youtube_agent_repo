import time
from datetime import datetime
from app.core.logger import logger

from app.services.agent_service import agent_service
from app.services.pipeline_service import pipeline_service


class SchedulerService:
    """
    Simple scheduler for running AI agents
    """

    def __init__(self):
        self.logger = logger

    def run_daily(self):

        self.logger.info("Scheduler started")

        while True:

            agents = self._get_all_active_agents()

            for agent in agents:
                try:
                    self.logger.info(f"Running agent: {agent['name']}")

                    pipeline_service.run(agent)

                except Exception as e:
                    self.logger.error(f"Agent failed: {e}")

            # wait 24 hours
            time.sleep(60 * 60 * 24)

    def _get_all_active_agents(self):
        return list(agent_service.list_user_agents(user_id=None))