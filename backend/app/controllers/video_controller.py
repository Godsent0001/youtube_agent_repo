from fastapi import HTTPException
from app.services.video.video_service import video_service
from app.core.logger import logger

class VideoController:
    """
    Controls lifecycle of MorphFlow videos
    """

    def __init__(self):
        self.logger = logger

    def get_user_videos(self, user_id: str):
        return video_service.get_user_videos(user_id)

    def get_video(self, video_id: str):
        video = video_service.get_video(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

    def delete_video(self, video_id: str):
        result = video_service.delete_video(video_id)
        self.logger.info(f"Video deleted: {video_id}")
        return result

video_controller = VideoController()
