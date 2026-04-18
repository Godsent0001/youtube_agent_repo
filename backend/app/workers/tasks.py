from app.services.pipeline_service import pipeline_service
from app.services.agent_service import agent_service
from app.core.logger import logger


class TaskService:
    """
    Defines async jobs for worker system
    """

    def __init__(self):
        self.logger = logger

    def generate_video_task(self, agent_id: str):

        """
        Full pipeline execution task
        """

        agent = agent_service.get_agent(agent_id)

        if not agent:
            self.logger.error(f"Agent not found: {agent_id}")
            return None

        self.logger.info(f"Running video generation task for {agent_id}")

        result = pipeline_service.run(agent)

        return result

    def retry_failed_video(self, payload: dict):

        """
        Retry failed pipeline execution
        """

        agent_id = payload.get("agent_id")

        self.logger.info(f"Retrying failed video for {agent_id}")

        return self.generate_video_task(agent_id)


task_service = TaskService()