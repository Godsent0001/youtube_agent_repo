from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from app.core.config import settings
from app.core.logger import logger


class YouTubeService:
    """
    Handles uploading videos to YouTube
    """

    def __init__(self):
        self.logger = logger

        # NOTE: You must implement OAuth token flow properly
        self.youtube = build(
            "youtube",
            "v3",
            developerKey=settings.YOUTUBE_CLIENT_SECRET
        )

    def upload_video(
        self,
        file_path: str,
        title: str,
        description: str,
        tags: list,
        content_type: str = "shorts"
    ):

        """
        Uploads video to YouTube
        """

        self.logger.info(f"Uploading video: {title}")

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"  # People & Blogs default
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


youtube_service = YouTubeService()