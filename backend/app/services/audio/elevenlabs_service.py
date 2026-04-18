import requests
from app.core.config import settings
from app.core.logger import logger
import uuid
import os


class ElevenLabsService:
    """
    Handles text-to-speech generation with mock fallback
    """

    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.logger = logger

    def generate_audio(self, text: str, voice_id: str = None):
        """
        Converts script to speech audio (or mocks it)
        """
        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join("storage/audio", file_name)
        os.makedirs("storage/audio", exist_ok=True)

        if self.api_key and "your_" not in self.api_key:
            voice_id = voice_id or "default_voice_id"
            url = f"{self.base_url}/{voice_id}"
            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2"
            }
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    self.logger.info(f"Audio generated: {file_path}")
                    return file_path
                else:
                    self.logger.error(f"ElevenLabs error: {response.text}")
            except Exception as e:
                self.logger.error(f"ElevenLabs request failed: {e}")

        # Mock fallback: create an empty file or just return path
        with open(file_path, "wb") as f:
            f.write(b"MOCK AUDIO CONTENT")
        self.logger.info(f"MOCK Audio generated: {file_path}")
        return file_path


elevenlabs_service = ElevenLabsService()
