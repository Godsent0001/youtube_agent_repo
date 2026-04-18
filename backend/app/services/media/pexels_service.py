import requests
from app.core.config import settings
from app.core.logger import logger


class PexelsService:
    """
    Handles fetching media from Pexels API with mock fallback
    """

    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com"
        self.logger = logger

    def search_images(self, query: str, per_page: int = 5):
        if self.api_key and "your_" not in self.api_key:
            try:
                url = f"{self.base_url}/v1/search"
                headers = {"Authorization": self.api_key}
                params = {"query": query, "per_page": per_page}
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return [
                        {"url": item["src"]["large"], "photographer": item["photographer"]}
                        for item in data.get("photos", [])
                    ]
                self.logger.error(f"Pexels error: {response.text}")
            except Exception as e:
                self.logger.error(f"Pexels search_images failed: {e}")

        # Mock fallback
        self.logger.info(f"Using mock results for Pexels images: {query}")
        return [{"url": f"https://images.pexels.com/mock_{i}.jpg", "photographer": "Mock Photographer"} for i in range(per_page)]

    def search_videos(self, query: str, per_page: int = 5):
        if self.api_key and "your_" not in self.api_key:
            try:
                url = f"{self.base_url}/videos/search"
                headers = {"Authorization": self.api_key}
                params = {"query": query, "per_page": per_page}
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    for video in data.get("videos", []):
                        if video["video_files"]:
                            best_file = video["video_files"][0]
                            results.append({"url": best_file["link"], "duration": video["duration"]})
                    return results
                self.logger.error(f"Pexels video error: {response.text}")
            except Exception as e:
                self.logger.error(f"Pexels search_videos failed: {e}")

        # Mock fallback
        self.logger.info(f"Using mock results for Pexels videos: {query}")
        return [{"url": f"https://videos.pexels.com/mock_{i}.mp4", "duration": 10} for i in range(per_page)]


pexels_service = PexelsService()
