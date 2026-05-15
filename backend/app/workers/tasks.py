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

        # Check if agent is still active
        if not agent.get("is_active", True):
            self.logger.info(f"Agent {agent_id} is paused. Skipping generation.")
            return None

        self.logger.info(f"Running video generation task for {agent_id}")

        try:
            result = pipeline_service.run(agent)

            # Update last run time
            from datetime import datetime
            agent_service.update_agent(agent_id, {"last_run_at": datetime.utcnow()})

            # Schedule NEXT run if agent is still active
            # We check again in case it was paused during generation
            updated_agent = agent_service.get_agent(agent_id)
            if updated_agent and updated_agent.get("is_active", True):
                self.logger.info(f"Scheduling next run for agent {agent_id} in 24 hours")

                # Use a Timer to avoid blocking the worker loop and handle the delay properly
                import threading

                def trigger_next_run():
                    # Check again if agent is still active before running
                    current_agent = agent_service.get_agent(agent_id)
                    if current_agent and current_agent.get("is_active", True):
                        # Avoid circular import by importing worker here
                        from app.workers.worker import worker
                        worker.add_job("generate_video", {"agent_id": agent_id})

                # 24 hours = 86400 seconds
                timer = threading.Timer(24 * 3600, trigger_next_run)
                timer.daemon = True
                timer.start()

            return result
        except Exception as e:
            self.logger.error(f"Pipeline failed for agent {agent_id}: {e}")
            raise e

    def retry_failed_video(self, payload: dict):

        """
        Retry failed pipeline execution
        """

        agent_id = payload.get("agent_id")

        self.logger.info(f"Retrying failed video for {agent_id}")

        return self.generate_video_task(agent_id)


task_service = TaskService()