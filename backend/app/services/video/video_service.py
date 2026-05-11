from bson import ObjectId
from pymongo.errors import PyMongoError

from app.db.session import videos_collection
from app.core.logger import logger


class VideoService:
    """
    Service for managing video-related operations.
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _prepare_video(self, video: dict | None):
        """
        Convert MongoDB _id -> id safely
        """

        if not video:
            return None

        # Create copy so original Mongo object is untouched
        prepared_video = dict(video)

        mongo_id = prepared_video.get("_id")

        if mongo_id:
            prepared_video["id"] = str(mongo_id)

        # Remove Mongo _id from API response
        prepared_video.pop("_id", None)

        return prepared_video

    # =========================
    # CREATE VIDEO
    # =========================
    def create_video(self, video_data: dict):
        """
        Create a new video document
        """

        try:
            result = videos_collection.insert_one(video_data)

            created_video = videos_collection.find_one(
                {"_id": result.inserted_id}
            )

            self.logger.info(
                f"Video created successfully: {result.inserted_id}"
            )

            return self._prepare_video(created_video)

        except PyMongoError as e:
            self.logger.error(f"Error creating video: {e}")
            return None

    # =========================
    # GET USER VIDEOS
    # =========================
    def get_user_videos(self, user_id: str):
        """
        Retrieve all videos belonging to a specific user.
        """

        try:
            videos = list(
                videos_collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1)
            )

            return [self._prepare_video(v) for v in videos]

        except PyMongoError as e:
            self.logger.error(
                f"Error retrieving videos for user {user_id}: {e}"
            )
            return []

    # =========================
    # GET SINGLE VIDEO
    # =========================
    def get_video(self, video_id: str):
        """
        Retrieve a single video by its ID.
        """

        try:
            if not ObjectId.is_valid(video_id):
                self.logger.warning(
                    f"Invalid ObjectId: {video_id}"
                )
                return None

            video = videos_collection.find_one(
                {"_id": ObjectId(video_id)}
            )

            return self._prepare_video(video)

        except Exception as e:
            self.logger.error(
                f"Error finding video by ID {video_id}: {e}"
            )
            return None

    # =========================
    # UPDATE VIDEO
    # =========================
    def update_video(self, video_id: str, update_data: dict):
        """
        Update a video document
        """

        try:
            if not ObjectId.is_valid(video_id):
                self.logger.warning(
                    f"Invalid ObjectId: {video_id}"
                )
                return None

            videos_collection.update_one(
                {"_id": ObjectId(video_id)},
                {"$set": update_data}
            )

            updated_video = videos_collection.find_one(
                {"_id": ObjectId(video_id)}
            )

            self.logger.info(
                f"Video updated successfully: {video_id}"
            )

            return self._prepare_video(updated_video)

        except PyMongoError as e:
            self.logger.error(
                f"Error updating video {video_id}: {e}"
            )
            return None

    # =========================
    # DELETE VIDEO
    # =========================
    def delete_video(self, video_id: str):
        """
        Delete a video by its ID.
        """

        try:
            if not ObjectId.is_valid(video_id):
                self.logger.warning(
                    f"Invalid ObjectId: {video_id}"
                )
                return False

            result = videos_collection.delete_one(
                {"_id": ObjectId(video_id)}
            )

            success = result.deleted_count > 0

            if success:
                self.logger.info(
                    f"Video deleted successfully: {video_id}"
                )
            else:
                self.logger.warning(
                    f"Video not found for deletion: {video_id}"
                )

            return success

        except PyMongoError as e:
            self.logger.error(
                f"Error deleting video {video_id}: {e}"
            )
            return False


# Singleton
video_service = VideoService()