import json
import re
import time
import google.generativeai as genai

from app.core.config import settings
from app.core.logger import logger


class LLMClient:
    """
    Gemini LLM wrapper (production-safe)
    - JSON-safe parsing
    - retry logic
    - better error handling
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.logger = logger

        self.model_name = "gemini-3-flash-preview"

        if not self.api_key and not settings.DEBUG:
            raise Exception("GEMINI_API_KEY is missing")

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None

        self.max_retries = 3

        self.logger.info(f"Gemini initialized with model: {self.model_name}")

    # =========================
    # CLEAN JSON EXTRACTION
    # =========================
    def _extract_json(self, text: str):
        """
        Extract JSON safely from LLM response
        """

        if not text:
            return ""

        # remove markdown code blocks
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

        return text.strip()

    # =========================
    # SAFE JSON PARSER
    # =========================
    def _safe_parse(self, text: str):
        try:
            return json.loads(text)
        except Exception:
            self.logger.error(f"JSON parse failed. Raw output:\n{text}")
            return None

    # =========================
    # MAIN GENERATE FUNCTION
    # =========================
    def generate(self, messages, temperature=0.7):

        prompt = ""

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt += f"{role.upper()}:\n{content}\n\n"

        last_error = None

        for attempt in range(self.max_retries):

            try:
                self.logger.info(f"Gemini request attempt {attempt + 1}")

                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature
                    }
                )

                if not response or not response.text:
                    raise Exception("Empty response from Gemini")

                cleaned = self._extract_json(response.text)

                return cleaned

            except Exception as e:
                last_error = e
                self.logger.warning(f"Gemini attempt {attempt + 1} failed: {e}")
                time.sleep(2 ** attempt)

        self.logger.error(f"Gemini failed after retries: {last_error}")
        raise last_error


llm_client = LLMClient()