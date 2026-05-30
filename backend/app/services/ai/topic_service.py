from app.core.logger import logger
from app.services.ai.ai_service import ai_service
import json

class TopicService:
    def __init__(self):
        self.logger = logger

    def generate_topic(self, niche: str, content_type: str = "shorts", custom_prompt: str = None):
        """
        Generate a viral video topic based on niche or custom prompt
        """
        prompt = f"""
        Generate a viral, high-engagement video topic for a {content_type} video.

        {f"The user's specific request is: {custom_prompt}" if custom_prompt else f"The niche is: {niche}"}

        The topic should be catchy, intriguing, and optimized for social media algorithms.
        Focus on creators like MrBeast, Alex Hormozi, or Ryan Trahan style of hooks.

        Return ONLY a JSON object with the following structure:
        {{
            "topic": "The catchy title/topic",
            "hook_strategy": "brief explanation of why this works",
            "target_audience": "who is this for"
        }}
        """

        try:
            response = ai_service.generate_text(prompt)
            # Strip any markdown formatting if present
            clean_response = response.strip().replace('```json', '').replace('```', '')
            return json.loads(clean_response)
        except Exception as e:
            self.logger.error(f"Topic generation failed: {e}")
            return {
                "topic": custom_prompt[:50] if custom_prompt else f"Amazing {niche} Video",
                "hook_strategy": "Generic appeal",
                "target_audience": "General"
            }

topic_service = TopicService()
