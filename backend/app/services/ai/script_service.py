import json
from app.services.ai.llm_client import llm_client
from app.core.logger import logger


class ScriptService:
    """
    LLM-powered script generator for viral YouTube content
    """

    def __init__(self):
        self.logger = logger

    def generate_script(self, topic: str, niche: str, content_type: str, research: dict):

        messages = [
            {
                "role": "system",
                "content": """
You are a world-class YouTube script writer specializing in viral content.

Your job:
- Write highly engaging scripts optimized for watch time
- Structure content for retention (hooks, tension, payoff)
- Adapt tone for Shorts or Long-form
- Use storytelling, curiosity loops, and emotional triggers
- Make content feel natural, not robotic

Return ONLY valid JSON:

{
  "script": "...",
  "hook": "...",
  "key_moments": ["...", "...", "..."],
  "cta": "..."
}
"""
            },
            {
                "role": "user",
                "content": f"""
Topic: {topic}
Niche: {niche}
Content Type: {content_type}

Research Data:
{json.dumps(research, indent=2)}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            return json.loads(response)
        except Exception as e:
            self.logger.error(f"Script generation failed: {e}")
            return {
                "script": "",
                "hook": "",
                "key_moments": [],
                "cta": ""
            }


script_service = ScriptService()