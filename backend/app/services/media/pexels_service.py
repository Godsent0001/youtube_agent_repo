import requests
from app.core.config import settings
from app.core.logger import logger


class PexelsService:
    """
    Handles fetching media from Pexels API
    """

    def __init__(self):
        self.api_key = settings.PEXELS_API_KEY
        self.base_url = "https://api.pexels.com"

        self.logger = logger

    def search_images(self, query: str, per_page: int = 5):

        url = f"{self.base_url}/v1/search"

        headers = {
            "Authorization": self.api_key
        }

        params = {
            "query": query,
            "per_page": per_page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            self.logger.error(f"Pexels error: {response.text}")
            return []

        data = response.json()

        results = [
            {
                "url": item["src"]["large"],
                "photographer": item["photographer"]
            }
            for item in data.get("photos", [])
        ]

        return results

    def search_videos(self, query: str, per_page: int = 5):

        url = f"{self.base_url}/videos/search"

        headers = {
            "Authorization": self.api_key
        }

        params = {
            "query": query,
            "per_page": per_page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            self.logger.error(f"Pexels video error: {response.text}")
            return []

        data = response.json()

        results = []

        for video in data.get("videos", []):
            best_file = video["video_files"][0]

            results.append({
                "url": best_file["link"],
                "duration": video["duration"]
            })

        return results


pexels_service = PexelsService()