from app.core.config import settings
from app.core.logger import logger

class YouTubeService:
    """
    Handles uploading videos to YouTube
    """

    def __init__(self):
        self.logger = logger
        self.youtube = None

        if settings.YOUTUBE_CLIENT_SECRET and "your_" not in settings.YOUTUBE_CLIENT_SECRET:
            try:
                from googleapiclient.discovery import build
                self.youtube = build(
                    "youtube",
                    "v3",
                    developerKey=settings.YOUTUBE_CLIENT_SECRET
                )
                self.logger.info("YouTube Service initialized with API key.")
            except Exception as e:
                self.logger.warning(f"Failed to initialize YouTube Service with API key: {e}. Falling back to mock.")
        else:
            self.logger.info("No YouTube API key provided. Using mock YouTube Service.")

    def upload_video(
        self,
        file_path: str,
        title: str,
        description: str,
        tags: list,
        thumbnail_path: str = None,
        content_type: str = "shorts"
    ):
        """
        Uploads video to YouTube (or mocks it)
        """
        self.logger.info(f"Uploading video: {title}")

        if self.youtube:
            try:
                from googleapiclient.http import MediaFileUpload
                request_body = {
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": "22"
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                }
                media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
                request = self.youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=media
                )
                response = request.execute()
                video_id = response.get("id")
                self.logger.info(f"Upload successful: {video_id}")
                return {
                    "video_id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
            except Exception as e:
                self.logger.error(f"YouTube upload failed: {e}. Returning mock data.")

        # Mock fallback
        import uuid
        mock_id = str(uuid.uuid4())
        self.logger.info(f"MOCK Upload successful: {mock_id}")
        return {
            "video_id": mock_id,
            "url": f"https://www.youtube.com/watch?v={mock_id}",
            "mock": True
        }

youtube_service = YouTubeService()
