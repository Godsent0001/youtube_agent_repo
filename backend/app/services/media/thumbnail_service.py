import os
import uuid
import requests
from app.core.logger import logger
from app.core.config import settings


class ThumbnailService:
    """
    Generates AI thumbnails with mock fallback
    """

    def __init__(self):
        self.logger = logger
        self.api_url = os.getenv("NANOBANANA_API_URL", "")
        self.api_key = os.getenv("NANOBANANA_API_KEY", "")

    def generate_thumbnail(self, title: str, script: str, niche: str):
        """
        Creates a thumbnail (or mocks it)
        """
        file_name = f"{uuid.uuid4()}.png"
        file_path = os.path.join("storage/images", file_name)
        os.makedirs("storage/images", exist_ok=True)

        if self.api_url and self.api_key and "your_" not in self.api_key:
            prompt = self._build_prompt(title, script, niche)
            try:
                response = requests.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "aspect_ratio": "16:9"
                    },
                    timeout=20
                )

                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    self.logger.info(f"Thumbnail created: {file_path}")
                    return file_path
                else:
                    self.logger.error(f"Thumbnail generation failed: {response.text}")
            except Exception as e:
                self.logger.error(f"Thumbnail request failed: {e}")

        # Mock fallback: create a dummy file
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1280, 720), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), f"Mock Thumbnail\n{title}", fill=(255,255,0))
        img.save(file_path)

        self.logger.info(f"MOCK Thumbnail created: {file_path}")
        return file_path

    def _build_prompt(self, title: str, script: str, niche: str):
        return f"Create a high CTR YouTube thumbnail for {title} in {niche} niche."

# Note: pipeline_service.py instantiates this, so we don't export an instance here if it expects a class
