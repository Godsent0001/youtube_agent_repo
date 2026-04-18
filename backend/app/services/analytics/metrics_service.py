from datetime import datetime
from app.core.logger import logger
from app.db.session import metrics_collection


class MetricsService:
    """
    Collects and stores video performance metrics
    """

    def __init__(self):
        self.logger = logger

    def record_metrics(self, video_id: str, agent_id: str, user_id: str, data: dict):

        """
        Expected data format (from YouTube API or scraper):
        {
            views: int,
            likes: int,
            comments: int,
            shares: int,
            avg_watch_time: float,
            retention_rate: float,
            ctr: float
        }
        """

        metrics_doc = {
            "video_id": video_id,
            "agent_id": agent_id,
            "user_id": user_id,

            "views": data.get("views", 0),
            "likes": data.get("likes", 0),
            "comments": data.get("comments", 0),
            "shares": data.get("shares", 0),

            "avg_watch_time": data.get("avg_watch_time", 0.0),
            "retention_rate": data.get("retention_rate", 0.0),
            "ctr": data.get("ctr", 0.0),

            "collected_at": datetime.utcnow()
        }

        metrics_collection.insert_one(metrics_doc)

        self.logger.info(f"Metrics stored for video: {video_id}")

        return metrics_doc

    def get_metrics_by_agent(self, agent_id: str):
        return list(metrics_collection.find({"agent_id": agent_id}))

    def get_metrics_by_video(self, video_id: str):
        return metrics_collection.find_one({"video_id": video_id})


metrics_service = MetricsService()