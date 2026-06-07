import json
import re

from app.services.ai.llm_client import llm_client
from app.core.logger import logger


class SceneService:
    """
    LLM-powered scene generator
    """

    def __init__(self):
        self.logger = logger

    def generate_scenes(self, script: str, content_type: str, video_length: str = None):
        messages = [
            {
                "role": "system",
                "content": """
You are a world-class video director.

YOUR JOB:
- Breakdown the script into visual scenes
- For each scene, provide a highly detailed visual description for image/video search
- Ensure scenes flow logically
- Keep scene durations proportional to text length

OUTPUT FORMAT (ONLY VALID JSON):
{
  "scenes": [
    {
      "text": "spoken narration for this scene",
      "visual_description": "detailed visual prompt",
      "duration_seconds": 5
    }
  ]
}
"""
            },
            {
                "role": "user",
                "content": f"Script: {script}\nContent Type: {content_type}\nTarget Length: {video_length}"
            }
        ]

        response = llm_client.generate(messages)

        try:
            cleaned = self._clean_response(response)
            parsed = json.loads(cleaned)
            return parsed.get("scenes", [])
        except Exception as e:
            self.logger.error(f"Scene generation failed: {e}")
            return []

    def _clean_response(self, text: str) -> str:
        if not text: return "{}"
        text = text.replace("```json", "").replace("```", "")
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match: return match.group(0)
        return text.strip()


scene_service = SceneService()
