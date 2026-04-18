from bson import ObjectId
from app.db.session import videos_collection
from app.core.logger import logger

class VideoService:
    """
    Service for managing Video-related operations.
    """
    def __init__(self):
        self.logger = logger

    def _prepare_video(self, video: dict):
        if video and "_id" in video:
            video["id"] = str(video.pop("_id"))
        return video

    def get_user_videos(self, user_id: str):
        """Retrieve all videos belonging to a specific user."""
        videos = list(videos_collection.find({"user_id": user_id}))
        return [self._prepare_video(v) for v in videos]

    def get_video(self, video_id: str):
        """Retrieve a single video by its ID."""
        try:
            video = videos_collection.find_one({"_id": ObjectId(video_id)})
            return self._prepare_video(video)
        except Exception as e:
            self.logger.error(f"Error finding video by ID {video_id}: {e}")
            return None

    def delete_video(self, video_id: str):
        """Delete a video by its ID."""
        try:
            result = videos_collection.delete_one({"_id": ObjectId(video_id)})
            return result.deleted_count > 0
        except Exception as e:
            self.logger.error(f"Error deleting video {video_id}: {e}")
            return False

video_service = VideoService()
