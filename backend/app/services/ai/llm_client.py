import json
import re
import google.generativeai as genai
from app.core.config import settings
from app.core.logger import logger

class LLMClient:
    """
    Gemini LLM wrapper with mock fallback (disabled in DEBUG=False)
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.logger = logger
        self.model_name = "gemini-2.0-flash-exp" # Using stable flash model name

        if self.api_key and "your_" not in self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.logger.info(f"Gemini LLM initialized with model: {self.model_name}")
        else:
            self.model = None
            if settings.DEBUG:
                self.logger.info("No Gemini API key provided. Using mock LLM responses.")
            else:
                self.logger.error("No Gemini API key provided and DEBUG=False. LLM will fail.")

    def _extract_json(self, text):
        """
        Cleans LLM response and extracts JSON
        """
        # Remove markdown code blocks if present
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        return text.strip()

    def generate(self, messages, temperature=0.7):
        if self.model:
            try:
                prompt = ""
                for msg in messages:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    prompt += f"{role.capitalize()}: {content}\n"

                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                    )
                )

                # Clean the response to ensure it's valid JSON if that's what's expected
                return self._extract_json(response.text)
            except Exception as e:
                if settings.DEBUG:
                    self.logger.warning(f"Gemini API call failed: {e}. Using mock response.")
                else:
                    self.logger.error(f"Gemini API call failed: {e}")
                    raise e

        if not settings.DEBUG:
            raise Exception("LLM Client not initialized and DEBUG=False")

        # Mock responses (only if DEBUG=True)
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
                {"description": "A high-tech laboratory with robots", "duration": 5, "visual_query": "futuristic lab robots", "emotion": "neutral"},
                {"description": "City of the future with flying cars", "duration": 5, "visual_query": "future city flying cars", "emotion": "action"},
                {"description": "Close up of a human eye reflecting code", "duration": 5, "visual_query": "human eye digital code reflection", "emotion": "shock"}
            ])

        if "metadata" in user_content:
            return json.dumps({
                "title": "The Future of AI is HERE!",
                "description": "Discover how AI is shaping our world in 2025.",
                "tags": ["AI", "Future", "Technology", "2025"]
            })

        return "This is a mock LLM response because no API key was provided or the API call failed."

llm_client = LLMClient()
