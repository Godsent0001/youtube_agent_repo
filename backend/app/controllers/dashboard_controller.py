from app.services.agent_service import agent_service
from app.services.video.video_service import video_service
from app.services.analytics.metrics_service import metrics_service
from app.core.logger import logger


class DashboardController:
    """
    Aggregates system analytics for frontend dashboard
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # OVERALL DASHBOARD
    # =========================
    def get_overview(self, user_id: str):

        agents = agent_service.list_user_agents(user_id)
        videos = video_service.get_user_videos(user_id)

        metrics = metrics_service.get_user_summary(user_id)

        return {
            "total_agents": len(agents),
            "total_videos": len(videos),

            "total_views": metrics.get("views", 0),
            "avg_retention": metrics.get("retention_rate", 0),
            "avg_ctr": metrics.get("ctr", 0)
        }

    # =========================
    # AGENT PERFORMANCE
    # =========================
    def get_agent_performance(self, agent_id: str):

        metrics = metrics_service.get_agent_metrics(agent_id)

        return {
            "agent_id": agent_id,
            "metrics": metrics
        }

    # =========================
    # ALL VIDEOS
    # =========================
    def get_videos(self, user_id: str):

        return video_service.get_user_videos(user_id)

    # =========================
    # SINGLE VIDEO ANALYTICS
    # =========================
    def get_video_details(self, video_id: str):

        video = video_service.get_video(video_id)
        metrics = metrics_service.get_video_metrics(video_id)

        return {
            "video": video,
            "metrics": metrics
        }

    # =========================
    # AI LEARNING INSIGHTS
    # =========================
    def get_insights(self, user_id: str):

        insights = metrics_service.generate_learning_insights(user_id)

        return {
            "insights": insights
        }

    # =========================
    # SYSTEM HEALTH METRICS
    # =========================
    def system_health(self):

        return {
            "status": "healthy",
            "worker": "running",
            "pipeline": "active"
        }


dashboard_controller = DashboardController()