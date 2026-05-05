import requests
from app.core.config import settings
from app.core.logger import logger


class PixabayService:
    """
    Handles fetching media from Pixabay API with mock fallback
    """

    def __init__(self):
        self.api_key = settings.PIXABAY_API_KEY
        self.base_url = "https://pixabay.com/api/"
        self.logger = logger

    def search_images(self, query: str, per_page: int = 5):
        if self.api_key and "your_" not in self.api_key:
            try:
                params = {
                    "key": self.api_key,
                    "q": query,
                    "image_type": "photo",
                    "per_page": per_page
                }
                response = requests.get(self.base_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return [
                        {"url": item["largeImageURL"], "photographer": item["user"]}
                        for item in data.get("hits", [])
                    ]
                self.logger.error(f"Pixabay error: {response.text}")
            except Exception as e:
                self.logger.error(f"Pixabay search_images failed: {e}")

        # Mock fallback
        self.logger.info(f"Using mock results for Pixabay images: {query}")
        return [{"url": f"https://pixabay.com/mock_{i}.jpg", "photographer": "Mock Photographer"} for i in range(per_page)]

    def search_videos(self, query: str, per_page: int = 5):
        if self.api_key and "your_" not in self.api_key:
            try:
                url = f"{self.base_url}videos/"
                params = {
                    "key": self.api_key,
                    "q": query,
                    "per_page": per_page
                }
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    for video in data.get("hits", []):
                        # Pixabay returns multiple resolutions in the 'videos' key
                        video_files = video.get("videos", {})
                        # Try to get a medium resolution like 'medium' or 'small'
                        best_file = video_files.get("medium") or video_files.get("small") or video_files.get("large") or video_files.get("tiny")
                        if best_file:
                            results.append({"url": best_file["url"], "duration": video["duration"]})
                    return results
                self.logger.error(f"Pixabay video error: {response.text}")
            except Exception as e:
                self.logger.error(f"Pixabay search_videos failed: {e}")

        # Mock fallback
        self.logger.info(f"Using mock results for Pixabay videos: {query}")
        return [{"url": f"https://pixabay.com/mock_{i}.mp4", "duration": 10} for i in range(per_page)]


pixabay_service = PixabayService()
