import requests
import json
from app.core.config import settings
from app.core.logger import logger

class LLMClient:
    """
    Generic LLM wrapper with mock fallback
    """

    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = "https://api.llm-provider.com/v1/chat/completions"  # replace
        self.logger = logger

    def generate(self, messages, temperature=0.7):
        if self.api_key and "your_" not in self.api_key:
            try:
                response = requests.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-4-maverick",
                        "messages": messages,
                        "temperature": temperature
                    },
                    timeout=10
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                self.logger.warning(f"LLM API call failed: {e}. Using mock response.")

        # Mock responses based on the system prompt or user content
        user_content = messages[-1]["content"].lower()

        if "topic" in user_content or "niche" in user_content:
            return json.dumps({
                "topic": "The Future of AI in 2025",
                "alternate_variations": ["AI Revolution", "How AI changes everything", "The dark side of AI"]
            })

        if "script" in user_content:
            return json.dumps({
                "script": "Welcome back to the channel. Today we are talking about the future of AI. Artificial intelligence is evolving faster than ever before. In this video, we'll explore what's next for humanity."
            })

        if "scene" in user_content:
            return json.dumps([
                {"description": "A high-tech laboratory with robots", "duration": 5},
                {"description": "City of the future with flying cars", "duration": 5},
                {"description": "Close up of a human eye reflecting code", "duration": 5}
            ])

        if "metadata" in user_content:
            return json.dumps({
                "title": "The Future of AI is HERE!",
                "description": "Discover how AI is shaping our world in 2025.",
                "tags": ["AI", "Future", "Technology", "2025"]
            })

        return "This is a mock LLM response because no API key was provided or the API call failed."

llm_client = LLMClient()
