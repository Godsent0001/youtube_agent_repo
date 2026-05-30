from app.core.logger import logger
from app.services.ai.ai_service import ai_service
import json

class ScriptService:
    def __init__(self):
        self.logger = logger

    def generate_script(self, topic: str, niche: str, content_type: str = "shorts", research: str = "", video_length: int = 60, custom_prompt: str = None):
        """
        Generate a full video script based on topic and research.
        """
        prompt = f"""
        Write a high-retention, viral video script for a {content_type} video.
        Topic: {topic}
        Target Length: {video_length} seconds.

        {f"User Input: {custom_prompt}" if custom_prompt else ""}
        Research context: {research}

        Guidelines:
        1. Start with a powerful hook in the first 3 seconds.
        2. Maintain fast pacing with clear transitions.
        3. Use emotional triggers or curiosity gaps.
        4. End with a strong call to action.
        5. Tone: Energetic, concise, and modern.

        Return ONLY a JSON object:
        {{
            "script": "The full spoken text of the video",
            "estimated_duration": {video_length},
            "pacing_notes": "e.g., fast, dramatic pauses"
        }}
        """

        try:
            response = ai_service.generate_text(prompt)
            clean_response = response.strip().replace('```json', '').replace('```', '')
            return json.loads(clean_response)
        except Exception as e:
            self.logger.error(f"Script generation failed: {e}")
            return {
                "script": f"Today we are talking about {topic}. This is going to be amazing. Make sure to watch until the end!",
                "estimated_duration": video_length,
                "pacing_notes": "Standard"
            }

script_service = ScriptService()
