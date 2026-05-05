from app.core.logger import logger
from app.services.media.pixabay_service import pixabay_service
from app.services.media.cache_service import cache_service


class SelectorService:
    """
    Selects best media for a scene using smart filtering
    """

    def __init__(self):
        self.logger = logger

    def get_best_media(self, scene: dict):

        query = scene.get("visual_query", "")
        emotion = scene.get("emotion", "neutral")

        # 1. Check cache first
        cached = cache_service.get(query)
        if cached:
            return cached

        # 2. Fetch from Pixabay
        images = pixabay_service.search_images(query)
        videos = pixabay_service.search_videos(query)

        # 3. Smart selection logic (lightweight, not LLM-based to avoid latency)
        selected = self._rank_media(images, videos, emotion)

        # 4. Cache result
        cache_service.set(query, selected)

        return selected

    def _rank_media(self, images, videos, emotion):

        """
        Select best media based on emotion + availability
        """

        if emotion in ["shock", "action"] and videos:
            return {
                "type": "video",
                "url": videos[0]["url"]
            }

        if images:
            return {
                "type": "image",
                "url": images[0]["url"]
            }

        if videos:
            return {
                "type": "video",
                "url": videos[0]["url"]
            }

        return {
            "type": "none",
            "url": None
        }


selector_service = SelectorService()