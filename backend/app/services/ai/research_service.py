import json
from app.core.logger import logger
from app.services.ai.llm_client import llm_client


class ResearchService:
    """
    LLM-driven research engine
    Produces structured insights about any topic
    """

    def __init__(self):
        self.logger = logger

    def generate_research(self, topic: str, niche: str):

        messages = [
            {
                "role": "system",
                "content": """
You are a research intelligence engine for a YouTube automation system.

Your job:
- Analyze the topic deeply
- Extract key insights
- Identify interesting angles for video content
- Make it feel current and engaging

Return ONLY valid JSON:
{
  "summary": "...",
  "key_points": ["...", "...", "..."],
  "angles": ["...", "..."],
  "hook_ideas": ["...", "..."]
}
"""
            },
            {
                "role": "user",
                "content": f"""
Topic: {topic}
Niche: {niche}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            return json.loads(response)
        except:
            self.logger.error("Research JSON parse failed")
            return {
                "summary": "",
                "key_points": [],
                "angles": [],
                "hook_ideas": []
            }


research_service = ResearchService()