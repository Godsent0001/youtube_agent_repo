import json
from app.services.ai.llm_client import llm_client
from app.core.logger import logger


class TopicService:
    """
    LLM-powered topic generator for YouTube AI agents
    """

    def __init__(self):
        self.logger = logger

    def generate_topic(self, niche: str, content_type: str, custom_prompt: str = None):

        messages = [
            {
                "role": "system",
                "content": """
You are a viral YouTube content strategist.

Your job:
- Generate highly clickable video ideas
- Focus on curiosity, emotion, controversy, or value
- Ensure ideas are optimized for YouTube Shorts or Long-form depending on input
- Avoid generic or boring ideas

Return ONLY valid JSON:
{
  "topic": "...",
  "alternate_variations": ["...", "...", "..."]
}
"""
            },
            {
                "role": "user",
                "content": f"""
Niche: {niche}
Content Type: {content_type}
Custom Direction: {custom_prompt if custom_prompt else "None"}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            return json.loads(response)
        except Exception as e:
            self.logger.error(f"Topic generation failed: {e}")
            return {
                "topic": "",
                "alternate_variations": []
            }


topic_service = TopicService()