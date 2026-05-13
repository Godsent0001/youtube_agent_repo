import os
import uuid
import time
import random

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from google import genai

from app.core.logger import logger
from app.core.config import settings


class ThumbnailService:
    """
    Production-ready AI thumbnail generator.

    FEATURES:
    - Imagen 4 generation
    - Automatic retries
    - Emergency fallback thumbnails
    - Better prompt engineering
    - Style randomization
    - Safer storage handling
    - Better title formatting
    """

    def __init__(self):

        self.logger = logger

        self.api_key = settings.GEMINI_API_KEY

        if (not self.api_key or "your_" in self.api_key) and not settings.DEBUG:
            raise Exception("Missing GEMINI_API_KEY")

        # ==========================================
        # GOOGLE CLIENT
        # ==========================================

        if self.api_key and "your_" not in self.api_key:
            self.client = genai.Client(
                api_key=self.api_key
            )
        else:
            self.client = None

        # ==========================================
        # IMAGEN MODEL
        # ==========================================

        self.image_model = (
            "models/imagen-4.0-generate-001"
        )

        # ==========================================
        # RETRIES
        # ==========================================

        self.max_retries = 3

        # ==========================================
        # THUMBNAIL STYLES
        # ==========================================

        self.styles = [
            "cinematic tech",
            "viral youtube",
            "dark mystery",
            "modern documentary",
            "high contrast futuristic",
            "neon cyberpunk",
            "dramatic storytelling"
        ]

        self.logger.info(
            f"ThumbnailService initialized with model: {self.image_model}"
        )

    # ==================================================
    # MAIN ENTRY
    # ==================================================

    def generate_thumbnail(
        self,
        title: str,
        script: str,
        niche: str
    ):

        os.makedirs(
            "storage/images",
            exist_ok=True
        )

        file_path = os.path.join(
            "storage/images",
            f"{uuid.uuid4()}.jpg"
        )

        prompt = self._build_imagen_prompt(
            title=title,
            script=script,
            niche=niche
        )

        # ==============================================
        # RETRY LOOP
        # ==============================================

        for attempt in range(self.max_retries):

            try:

                self.logger.info(
                    f"Generating thumbnail with Imagen 4 (attempt {attempt + 1})..."
                )

                result = self.client.models.generate_images(
                    model=self.image_model,
                    prompt=prompt,
                    config={
                        "number_of_images": 1,
                        "aspect_ratio": "16:9",
                        "output_mime_type": "image/jpeg",
                        "person_generation": "ALLOW_ADULT"
                    }
                )

                if not result.generated_images:

                    raise Exception(
                        "No image returned from Imagen"
                    )

                generated_image = (
                    result.generated_images[0]
                )

                # Ensure image is in RGB format for JPEG saving
                img = generated_image.image
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                img.save(
                    file_path,
                    "JPEG",
                    quality=95
                )

                # ======================================
                # VALIDATE FILE
                # ======================================

                if not os.path.exists(file_path):

                    raise Exception(
                        "Thumbnail file missing after save"
                    )

                if os.path.getsize(file_path) < 1000:

                    raise Exception(
                        "Generated thumbnail corrupted"
                    )

                self.logger.info(
                    f"Thumbnail generated successfully: {file_path}"
                )

                return file_path

            except Exception as e:

                self.logger.error(
                    f"Thumbnail generation failed on attempt {attempt + 1}: {e}"
                )

                # exponential backoff
                time.sleep(2 ** attempt)

        # ==============================================
        # FALLBACK THUMBNAIL
        # ==============================================

        self.logger.warning(
            "Using emergency fallback thumbnail"
        )

        return self._generate_fallback_thumbnail(
            title=title,
            output_path=file_path
        )

    # ==================================================
    # FALLBACK THUMBNAIL
    # ==================================================

    def _generate_fallback_thumbnail(
        self,
        title: str,
        output_path: str
    ):

        try:

            width = 1280
            height = 720

            # ==========================================
            # RANDOM DARK BACKGROUND
            # ==========================================

            backgrounds = [
                (10, 10, 10),
                (20, 20, 35),
                (15, 15, 25),
                (5, 5, 5),
                (12, 18, 28)
            ]

            bg_color = random.choice(backgrounds)

            image = Image.new(
                "RGB",
                (width, height),
                bg_color
            )

            draw = ImageDraw.Draw(image)

            # ==========================================
            # ACCENT BAR
            # ==========================================

            accent_colors = [
                (255, 0, 0),
                (0, 255, 180),
                (255, 215, 0),
                (0, 140, 255),
                (255, 80, 80)
            ]

            accent = random.choice(
                accent_colors
            )

            draw.rectangle(
                [(0, 0), (25, height)],
                fill=accent
            )

            # ==========================================
            # CLEAN TITLE
            # ==========================================

            clean_title = self._shorten_title(
                title
            )

            # ==========================================
            # FONT
            # ==========================================

            try:

                font = ImageFont.truetype(
                    "arial.ttf",
                    70
                )

            except:

                font = ImageFont.load_default()

            # ==========================================
            # WORD WRAP
            # ==========================================

            wrapped = self._wrap_text(
                clean_title,
                draw,
                font,
                900
            )

            # ==========================================
            # DRAW TEXT
            # ==========================================

            y = 180

            for line in wrapped:

                bbox = draw.textbbox(
                    (0, 0),
                    line,
                    font=font
                )

                line_width = bbox[2] - bbox[0]

                x = (
                    width - line_width
                ) // 2

                # shadow
                draw.text(
                    (x + 4, y + 4),
                    line,
                    font=font,
                    fill="black"
                )

                # text
                draw.text(
                    (x, y),
                    line,
                    font=font,
                    fill="white"
                )

                y += 100

            # ==========================================
            # SAVE
            # ==========================================

            image.save(
                output_path,
                quality=95
            )

            self.logger.info(
                f"Fallback thumbnail created: {output_path}"
            )

            return output_path

        except Exception as e:

            self.logger.error(
                f"Fallback thumbnail failed: {e}"
            )

            raise e

    # ==================================================
    # TITLE SHORTENER
    # ==================================================

    def _shorten_title(
        self,
        title: str
    ):

        if not title:
            return "AI VIDEO"

        title = title.strip()

        if len(title) <= 55:
            return title

        shortened = title[:55]

        if " " in shortened:
            shortened = shortened.rsplit(
                " ",
                1
            )[0]

        return shortened + "..."

    # ==================================================
    # TEXT WRAPPER
    # ==================================================

    def _wrap_text(
        self,
        text,
        draw,
        font,
        max_width
    ):

        words = text.split()

        lines = []

        current = ""

        for word in words:

            test = (
                current + " " + word
            ).strip()

            bbox = draw.textbbox(
                (0, 0),
                test,
                font=font
            )

            width = bbox[2] - bbox[0]

            if width <= max_width:
                current = test
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines[:4]

    # ==================================================
    # PROMPT ENGINE
    # ==================================================

    def _build_imagen_prompt(
        self,
        title: str,
        script: str,
        niche: str
    ):

        short_context = script[:400]

        style = random.choice(
            self.styles
        )

        clean_title = self._shorten_title(
            title
        )

        return f"""
Create a HIGH click-through-rate professional YouTube thumbnail.

VIDEO INFO:
Title: {clean_title}
Niche: {niche}
Context: {short_context}

STYLE:
{style}

OBJECTIVE:
Design a visually irresistible thumbnail optimized for maximum CTR.

IMPORTANT RULES:
- Create ONE powerful visual focus
- Strong emotional storytelling
- Cinematic lighting
- High contrast
- Modern YouTube thumbnail quality
- Avoid clutter
- Make subject large and obvious
- Mobile friendly composition
- Viral YouTube energy
- Dramatic composition
- Clear depth of field
- Professional polish

TEXT RULES:
- Text should be minimal
- Bold readable text only if necessary
- Avoid too much wording

OUTPUT:
Generate ONE cinematic 16:9 YouTube thumbnail image.
"""

# ==================================================
# SINGLETON
# ==================================================

thumbnail_service = ThumbnailService()