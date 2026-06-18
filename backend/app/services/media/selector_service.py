import random

from app.core.logger import logger
from app.services.media.pixabay_service import pixabay_service
from app.services.media.cache_service import cache_service


class SelectorService:
    """
    Video-first smart media selector

    Improvements:
    - respects scene media_type_preference
    - uses stock_query (not noisy visual_query)
    - stronger video prioritization
    - better fallback logic
    - reduced randomness for consistency
    """

    def __init__(self):
        self.logger = logger
        self.used_media_urls = set()

    # =====================================
    # MAIN ENTRY
    # =====================================

    def get_best_media(self, scene: dict):

        query = (
            scene.get("stock_query")
            or scene.get("visual_query")
            or scene.get("visual_description", "")
        ).strip()

        emotion = scene.get("emotion", "neutral")
        preferred = scene.get("media_type_preference", "image")

        if not query:
            return {"type": "none", "url": None}

        self.logger.info(f"Searching media for: {query}")

        # =====================================
        # CACHE CHECK
        # =====================================

        cached = cache_service.get(query)

        if cached and cached.get("url") not in self.used_media_urls:
            self.used_media_urls.add(cached["url"])
            return cached

        # =====================================
        # FETCH MEDIA
        # =====================================

        images = pixabay_service.search_images(query, per_page=10)
        videos = pixabay_service.search_videos(query, per_page=10)

        self.logger.info(
            f"Pixabay returned {len(images)} images and {len(videos)} videos"
        )

        # remove duplicates
        images = self._remove_used(images)
        videos = self._remove_used(videos)

        # =====================================
        # SMART SELECTION (NEW CORE LOGIC)
        # =====================================

        selected = self._select_best(
            images=images,
            videos=videos,
            emotion=emotion,
            preferred=preferred
        )

        if selected.get("url"):
            self.used_media_urls.add(selected["url"])

        cache_service.set(query, selected)

        return selected

    # =====================================
    # CORE DECISION ENGINE
    # =====================================

    def _select_best(self, images, videos, emotion, preferred):

        video_emotions = {
            "shock", "action", "fear", "excitement", "dramatic", "tension"
        }

        # =====================================
        # RULE 1: FORCE VIDEO IF REQUESTED
        # =====================================

        if preferred == "video" and videos:
            self.logger.info("Forced video selection from scene preference")

            return {
                "type": "video",
                "url": random.choice(videos)["url"]
            }

        # =====================================
        # RULE 2: EMOTION-BASED VIDEO PRIORITY
        # =====================================

        if emotion in video_emotions and videos:
            self.logger.info("Emotion triggered video selection")

            return {
                "type": "video",
                "url": random.choice(videos)["url"]
            }

        # =====================================
        # RULE 3: BALANCED VIDEO USAGE (IMPORTANT FIX)
        # =====================================

        if videos and random.random() < 0.7:
            self.logger.info("Balanced video selection (70% chance)")

            return {
                "type": "video",
                "url": random.choice(videos)["url"]
            }

        # =====================================
        # RULE 4: IMAGE FALLBACK
        # =====================================

        if images:
            self.logger.info("Selected image media")

            return {
                "type": "image",
                "url": random.choice(images)["url"]
            }

        # =====================================
        # RULE 5: VIDEO FALLBACK
        # =====================================

        if videos:
            self.logger.info("Fallback video selected")

            return {
                "type": "video",
                "url": random.choice(videos)["url"]
            }

        # =====================================
        # FINAL FALLBACK
        # =====================================

        self.logger.warning("No media found")

        return {
            "type": "none",
            "url": None
        }

    # =====================================
    # REMOVE DUPLICATES
    # =====================================

    def _remove_used(self, media_list):

        return [
            m for m in media_list
            if m.get("url") and m["url"] not in self.used_media_urls
        ]


selector_service = SelectorService()