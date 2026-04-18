import json
from app.core.logger import logger
from app.services.ai.llm_client import llm_client


class MetadataService:
    """
    Generates YouTube SEO metadata using LLM
    """

    def __init__(self):
        self.logger = logger

    def generate_metadata(self, topic: str, script: str, niche: str):

        messages = [
            {
                "role": "system",
                "content": """
You are a YouTube growth expert.

Your job:
- Create viral titles optimized for CTR
- Write SEO-optimized descriptions
- Generate relevant tags/hashtags
- Maximize engagement probability

Return ONLY valid JSON:
{
  "title": "...",
  "description": "...",
  "tags": ["...", "...", "..."]
}
"""
            },
            {
                "role": "user",
                "content": f"""
Topic: {topic}
Niche: {niche}
Script:
{script}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            return json.loads(response)
        except:
            self.logger.error("Metadata JSON parse failed")
            return {
                "title": "",
                "description": "",
                "tags": []
            }


metadata_service = MetadataService()