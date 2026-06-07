from app.services.video.video_service import video_service
from app.core.logger import logger


class DashboardController:
    """
    Aggregates system data for MorphFlow dashboard
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # OVERALL DASHBOARD
    # =========================
    def get_overview(self, user_id: str):
        videos = video_service.get_user_videos(user_id)

        return {
            "total_videos": len(videos),
            "recent_videos": videos[:5]
        }

    # =========================
    # ALL VIDEOS
    # =========================
    def get_videos(self, user_id: str):
        return video_service.get_user_videos(user_id)

    # =========================
    # SINGLE VIDEO DETAILS
    # =========================
    def get_video_details(self, video_id: str):
        video = video_service.get_video(video_id)
        return {
            "video": video
        }


dashboard_controller = DashboardController()
