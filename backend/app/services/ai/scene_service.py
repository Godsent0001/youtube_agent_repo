import json
from app.core.logger import logger
from app.services.ai.llm_client import llm_client


class SceneService:
    """
    Converts script into structured video scenes using LLM
    """

    def __init__(self):
        self.logger = logger

    def generate_scenes(self, script: str, content_type: str):

        messages = [
            {
                "role": "system",
                "content": """
You are a senior video director for viral YouTube content.

Your job:
- Break scripts into high-retention scenes
- Assign visual directions (for stock footage APIs like Pexels)
- Optimize pacing for engagement
- Ensure emotional flow

Return ONLY valid JSON:
{
  "scenes": [
    {
      "text": "...",
      "visual_query": "...",
      "duration_seconds": 0
    }
  ]
}
"""
            },
            {
                "role": "user",
                "content": f"""
Content Type: {content_type}

Script:
{script}
"""
            }
        ]

        response = llm_client.generate(messages)

        try:
            return json.loads(response)["scenes"]
        except:
            self.logger.error("Scene parsing failed")
            return []


scene_service = SceneService()