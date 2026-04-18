from fastapi import HTTPException

from app.services.video.video_service import video_service
from app.services.analytics.metrics_service import metrics_service
from app.workers.worker import worker
from app.core.logger import logger


class VideoController:
    """
    Controls full lifecycle of AI-generated videos
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # GET USER VIDEOS
    # =========================
    def get_user_videos(self, user_id: str):

        return video_service.get_user_videos(user_id)

    # =========================
    # GET SINGLE VIDEO
    # =========================
    def get_video(self, video_id: str):

        video = video_service.get_video(video_id)

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        metrics = metrics_service.get_video_metrics(video_id)

        return {
            "video": video,
            "metrics": metrics
        }

    # =========================
    # DELETE VIDEO
    # =========================
    def delete_video(self, video_id: str):

        result = video_service.delete_video(video_id)

        self.logger.info(f"Video deleted: {video_id}")

        return result

    # =========================
    # REGENERATE VIDEO
    # =========================
    def regenerate_video(self, video_id: str):

        video = video_service.get_video(video_id)

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        worker.add_job("generate_video", {
            "agent_id": video["agent_id"]
        })

        self.logger.info(f"Video regeneration triggered: {video_id}")

        return {
            "message": "Video regeneration started",
            "video_id": video_id
        }

    # =========================
    # RETRY FAILED VIDEO
    # =========================
    def retry_video(self, video_id: str):

        video = video_service.get_video(video_id)

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        if video.get("upload_status") != "failed":
            return {
                "message": "Video is not in failed state"
            }

        worker.add_job("generate_video", {
            "agent_id": video["agent_id"]
        })

        self.logger.info(f"Retry initiated: {video_id}")

        return {
            "message": "Retry started",
            "video_id": video_id
        }

    # =========================
    # VIDEO STATUS
    # =========================
    def get_status(self, video_id: str):

        video = video_service.get_video(video_id)

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        return {
            "video_id": video_id,
            "status": video.get("upload_status"),
            "stage": video.get("current_stage", "unknown")
        }


video_controller = VideoController()