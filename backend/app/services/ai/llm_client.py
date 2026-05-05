import json
import google.generativeai as genai
from app.core.config import settings
from app.core.logger import logger

class LLMClient:
    """
    Gemini LLM wrapper with mock fallback
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.logger = logger
        self.model_name = "gemini-1.5-flash" # Defaulting to flash for speed/cost

        if self.api_key and "your_" not in self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.logger.info(f"Gemini LLM initialized with model: {self.model_name}")
        else:
            self.model = None
            self.logger.info("No Gemini API key provided. Using mock LLM responses.")

    def generate(self, messages, temperature=0.7):
        if self.model:
            try:
                # Convert messages to Gemini format
                # Gemini expects a prompt string or a list of parts.
                # For simplicity, we'll join the messages into a single prompt if it's more than just a user message.

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
                return response.text
            except Exception as e:
                self.logger.warning(f"Gemini API call failed: {e}. Using mock response.")

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
