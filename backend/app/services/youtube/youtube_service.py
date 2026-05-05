import uuid
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.core.config import settings
from app.core.logger import logger
from app.services.user_service import user_service
from app.db.session import users_collection

class YouTubeService:
    """
    Handles uploading videos to YouTube using per-user OAuth tokens
    """

    def __init__(self):
        self.logger = logger

    def _get_credentials_for_user(self, user_id: str):
        """
        Retrieves and refreshes OAuth credentials for a specific user
        """
        user = user_service.get_by_id(user_id)
        if not user:
             self.logger.warning(f"User {user_id} not found")
             return None

        # In case it's a dict (from DB) or an object (from Pydantic)
        refresh_token = user.get("youtube_refresh_token") if isinstance(user, dict) else getattr(user, "youtube_refresh_token", None)
        access_token = user.get("youtube_access_token") if isinstance(user, dict) else getattr(user, "youtube_access_token", None)

        if not refresh_token:
            self.logger.warning(f"No YouTube refresh token found for user {user_id}")
            return None

        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.YOUTUBE_CLIENT_ID,
            client_secret=settings.YOUTUBE_CLIENT_SECRET,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )

        if not creds.valid:
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Update tokens in DB
                    users_collection.update_one(
                        {"_id": user["_id"]},
                        {"$set": {
                            "youtube_access_token": creds.token,
                            "youtube_token_expiry": creds.expiry
                        }}
                    )
                except Exception as e:
                    self.logger.error(f"Failed to refresh YouTube token for user {user_id}: {e}")
                    return None
            else:
                return None

        return creds

    def upload_video(
        self,
        user_id: str,
        file_path: str,
        title: str,
        description: str,
        tags: list,
        thumbnail_path: str = None,
        content_type: str = "shorts"
    ):
        """
        Uploads video to YouTube (or mocks it if DEBUG=True)
        """
        self.logger.info(f"Uploading video for user {user_id}: {title}")

        creds = self._get_credentials_for_user(user_id)

        if creds:
            try:
                youtube = build("youtube", "v3", credentials=creds)
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
                request = youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=media
                )
                response = request.execute()
                video_id = response.get("id")

                if video_id and thumbnail_path and os.path.exists(thumbnail_path):
                    try:
                        youtube.thumbnails().set(
                            videoId=video_id,
                            media_body=MediaFileUpload(thumbnail_path)
                        ).execute()
                        self.logger.info(f"Thumbnail uploaded for video {video_id}")
                    except Exception as te:
                        self.logger.error(f"Failed to upload thumbnail: {te}")

                self.logger.info(f"Upload successful: {video_id}")
                return {
                    "video_id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
            except Exception as e:
                self.logger.error(f"YouTube upload failed: {e}")
                if not settings.DEBUG:
                    raise e

        if not settings.DEBUG:
            raise Exception(f"No valid YouTube credentials for user {user_id} and DEBUG=False")

        # Mock fallback (only if DEBUG=True)
        mock_id = str(uuid.uuid4())
        self.logger.info(f"MOCK Upload successful: {mock_id}")
        return {
            "video_id": mock_id,
            "url": f"https://www.youtube.com/watch?v={mock_id}",
            "mock": True
        }

youtube_service = YouTubeService()
