import os
import uuid
import requests
from app.core.logger import logger
from app.core.config import settings


class ThumbnailService:
    """
    Generates AI thumbnails using external image model (NanoBanana or equivalent)
    """

    def __init__(self):
        self.logger = logger

        # Replace with NanoBanana endpoint
        self.api_url = os.getenv("NANOBANANA_API_URL", "")
        self.api_key = os.getenv("NANOBANANA_API_KEY", "")

    def generate_thumbnail(self, title: str, script: str, niche: str):

        """
        Creates a viral thumbnail prompt and sends to image model
        """

        prompt = self._build_prompt(title, script, niche)

        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "aspect_ratio": "16:9"
            }
        )

        if response.status_code != 200:
            self.logger.error(f"Thumbnail generation failed: {response.text}")
            return None

        image_data = response.content

        file_name = f"{uuid.uuid4()}.png"
        file_path = os.path.join("storage/images", file_name)

        os.makedirs("storage/images", exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(image_data)

        self.logger.info(f"Thumbnail created: {file_path}")

        return file_path

    def _build_prompt(self, title: str, script: str, niche: str):

        """
        IMPORTANT: No hardcoding styles — let model decide from prompt only
        """

        return f"""
Create a high CTR YouTube thumbnail.

Context:
Title: {title}
Niche: {niche}

Script Summary:
{script[:500]}

Requirements:
- Extremely eye-catching
- Emotional or curiosity-driven
- Bold composition for mobile viewing
- High contrast visuals
- Professional YouTube style
"""