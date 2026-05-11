import os
import time
import uuid
import requests

from app.core.config import settings
from app.core.logger import logger


class ElevenLabsService:
    """
    Production-grade ElevenLabs TTS service

    Fixes:
    - timeout issues
    - retry logic improvements
    - script cleaning (removes numbering issues)
    - safer request handling
    - better failure fallback
    """

    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.logger = logger

        self.timeout = 60
        self.max_retries = 3

    # =========================
    # MAIN ENTRY
    # =========================
    def generate_audio(self, text: str, voice_id: str = None):

        os.makedirs("storage/audio", exist_ok=True)

        file_path = os.path.join(
            "storage/audio",
            f"{uuid.uuid4()}.mp3"
        )

        # =========================
        # VALIDATE
        # =========================
        if not self.api_key or "your_" in self.api_key:
            return self._mock_audio(file_path)

        # clean script before sending
        text = self._clean_text(text)

        # prevent overly long requests (important fix)
        text = self._limit_length(text)

        voice_id = voice_id or settings.ELEVENLABS_VOICE_ID or "wWWn96OtTHu1sn8SRGEr"

        url = f"{self.base_url}/{voice_id}"

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        # =========================
        # RETRY LOOP
        # =========================
        for attempt in range(self.max_retries):

            try:
                self.logger.info(
                    f"ElevenLabs TTS attempt {attempt + 1}"
                )

                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )

                # SUCCESS
                if response.status_code == 200:

                    with open(file_path, "wb") as f:
                        f.write(response.content)

                    self.logger.info(f"Audio generated: {file_path}")

                    return file_path

                # BAD REQUEST → DO NOT RETRY
                if response.status_code == 400:
                    self.logger.error(
                        f"Bad request (400): {response.text}"
                    )
                    break

                # AUTH ERROR → STOP
                if response.status_code == 401:
                    self.logger.error("Invalid ElevenLabs API key")
                    break

                self.logger.error(
                    f"ElevenLabs error {response.status_code}: {response.text}"
                )

            except requests.exceptions.Timeout:
                self.logger.warning(
                    f"Timeout attempt {attempt + 1}"
                )

            except Exception as e:
                self.logger.error(f"ElevenLabs exception: {e}")

            # exponential backoff
            time.sleep(2 ** attempt)

        # fallback
        return self._fallback(file_path)

    # =========================
    # TEXT CLEANING (IMPORTANT FIX)
    # =========================
    def _clean_text(self, text: str):

        if not text:
            return ""

        import re

        # remove numbering issues (ROOT CAUSE OF "003", "004")
        text = re.sub(r"\b\d+\.\s*", "", text)
        text = re.sub(r"\b0+\d+\b", "", text)

        # remove scene markers
        text = re.sub(r"\b(scene|step)\s*\d+\b", "", text, flags=re.IGNORECASE)

        # normalize spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # =========================
    # LENGTH LIMIT (IMPORTANT)
    # =========================
    def _limit_length(self, text: str, max_chars: int = 4500):

        if len(text) <= max_chars:
            return text

        return text[:max_chars]

    # =========================
    # MOCK AUDIO
    # =========================
    def _mock_audio(self, file_path):

        with open(file_path, "wb") as f:
            f.write(b"MOCK AUDIO CONTENT")

        self.logger.info(f"MOCK audio generated: {file_path}")

        return file_path

    # =========================
    # FINAL FALLBACK
    # =========================
    def _fallback(self, file_path):

        if settings.DEBUG:
            return self._mock_audio(file_path)

        raise Exception(
            "ElevenLabs failed after retries (production mode)"
        )


# singleton
elevenlabs_service = ElevenLabsService()