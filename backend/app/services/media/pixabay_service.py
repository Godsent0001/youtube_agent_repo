import random
import time
import requests

from app.core.config import settings
from app.core.logger import logger


class PixabayService:
    """
    Production-grade Pixabay media engine

    FIXES:
    - API timeouts (retry system)
    - missing video reliability
    - better query fallback
    - strict media validation
    - improved ranking stability
    """

    def __init__(self):

        self.api_key = settings.PIXABAY_API_KEY
        self.base_url = "https://pixabay.com/api/"
        self.logger = logger

        # retry config
        self.max_retries = 3
        self.retry_delay = 1.2

    # ==================================================
    # IMAGE SEARCH (WITH RETRY)
    # ==================================================

    def search_images(self, query: str, per_page: int = 15):

        query = self._sanitize_query(query)
        per_page = max(3, min(50, per_page))

        if not self._has_api():
            return self._mock_images(per_page)

        for attempt in range(self.max_retries):

            try:
                params = {
                    "key": self.api_key,
                    "q": query,
                    "image_type": "photo",
                    "orientation": "horizontal",
                    "safesearch": "true",
                    "order": "popular",
                    "per_page": per_page
                }

                response = requests.get(
                    self.base_url,
                    params=params,
                    timeout=10
                )

                if response.status_code != 200:
                    raise Exception(response.text)

                data = response.json()
                hits = data.get("hits", [])

                images = []

                for item in hits:

                    url = (
                        item.get("largeImageURL")
                        or item.get("webformatURL")
                    )

                    if not url:
                        continue

                    images.append({
                        "url": url,
                        "views": item.get("views", 0),
                        "likes": item.get("likes", 0),
                        "downloads": item.get("downloads", 0),
                        "width": item.get("imageWidth", 0),
                        "height": item.get("imageHeight", 0),
                        "type": "image"
                    })

                if images:
                    ranked = self._rank_images(images)

                    self.logger.info(
                        f"Pixabay images OK: {len(ranked)} | {query}"
                    )

                    return ranked

                raise Exception("No images returned")

            except Exception as e:

                self.logger.warning(
                    f"Image retry {attempt+1}/{self.max_retries} failed: {e}"
                )

                time.sleep(self.retry_delay)

        return self._mock_images(per_page)

    # ==================================================
    # VIDEO SEARCH (WITH RETRY + STRONG VALIDATION)
    # ==================================================

    def search_videos(self, query: str, per_page: int = 10):

        query = self._sanitize_query(query)
        per_page = max(3, min(30, per_page))

        if not self._has_api():
            return self._mock_videos(per_page)

        url = f"{self.base_url}videos/"

        for attempt in range(self.max_retries):

            try:
                params = {
                    "key": self.api_key,
                    "q": query,
                    "safesearch": "true",
                    "order": "popular",
                    "per_page": per_page
                }

                response = requests.get(
                    url,
                    params=params,
                    timeout=12
                )

                if response.status_code != 200:
                    raise Exception(response.text)

                data = response.json()
                hits = data.get("hits", [])

                videos = []

                for item in hits:

                    files = item.get("videos", {})

                    # STRICT video selection priority
                    best_file = (
                        files.get("large")
                        or files.get("medium")
                        or files.get("small")
                    )

                    if not best_file:
                        continue

                    video_url = best_file.get("url")

                    if not video_url:
                        continue

                    videos.append({
                        "url": video_url,
                        "duration": item.get("duration", 10),
                        "width": best_file.get("width", 0),
                        "height": best_file.get("height", 0),
                        "views": item.get("views", 0),
                        "downloads": item.get("downloads", 0),
                        "type": "video"
                    })

                if videos:
                    ranked = self._rank_videos(videos)

                    self.logger.info(
                        f"Pixabay videos OK: {len(ranked)} | {query}"
                    )

                    return ranked

                raise Exception("No videos returned")

            except Exception as e:

                self.logger.warning(
                    f"Video retry {attempt+1}/{self.max_retries} failed: {e}"
                )

                time.sleep(self.retry_delay)

        return self._mock_videos(per_page)

    # ==================================================
    # IMAGE RANKING
    # ==================================================

    def _rank_images(self, images: list):

        def score(img):
            return (
                img.get("likes", 0) * 3 +
                img.get("downloads", 0) * 2 +
                img.get("views", 0)
            )

        ranked = sorted(images, key=score, reverse=True)

        top = ranked[:10]

        random.shuffle(top)

        return top

    # ==================================================
    # VIDEO RANKING (STRONGER PRIORITY)
    # ==================================================

    def _rank_videos(self, videos: list):

        def score(v):
            return (
                v.get("width", 0) +
                v.get("height", 0) +
                (v.get("duration", 0) * 4) +
                v.get("views", 0) * 2
            )

        ranked = sorted(videos, key=score, reverse=True)

        top = ranked[:8]

        random.shuffle(top)

        return top

    # ==================================================
    # QUERY CLEANING (IMPORTANT FIX)
    # ==================================================

    def _sanitize_query(self, query: str):

        if not query:
            return "technology"

        query = query.strip().lower()

        query = query.replace('"', "")
        query = query.replace("'", "")

        # remove overly long prompts (AI scene bug fix)
        if len(query) > 80:
            query = query[:80]

        return query

    # ==================================================
    # API CHECK
    # ==================================================

    def _has_api(self):

        return self.api_key and "your_" not in self.api_key

    # ==================================================
    # MOCKS
    # ==================================================

    def _mock_images(self, per_page):

        self.logger.warning("Using mock images")

        return [
            {
                "url": f"https://pixabay.com/mock_image_{i}.jpg",
                "type": "image"
            }
            for i in range(per_page)
        ]

    def _mock_videos(self, per_page):

        self.logger.warning("Using mock videos")

        return [
            {
                "url": f"https://pixabay.com/mock_video_{i}.mp4",
                "duration": 10,
                "type": "video"
            }
            for i in range(per_page)
        ]


pixabay_service = PixabayService()