import os
import uuid
import requests
import numpy as np

from PIL import Image, ImageDraw, ImageFont

from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    ColorClip
)

from app.core.logger import logger
from app.services.video.effects_service import effects_service


# ==================================================
# PILLOW FIX
# ==================================================
if not hasattr(Image, "ANTIALIAS"):
    if hasattr(Image, "Resampling"):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    else:
        Image.ANTIALIAS = Image.BICUBIC


class VideoBuilderService:

    def __init__(self):
        self.logger = logger
        self.temp_dir = "storage/temp_media"
        os.makedirs(self.temp_dir, exist_ok=True)

    # ==================================================
    # MAIN PIPELINE
    # ==================================================
    def build_video(self, scenes: list, audio_path: str, output_path: str):

        self.logger.info("Starting video build process")

        clips = []

        # preload audio (IMPORTANT FIX: prevents late freeze)
        audio = None
        audio_duration = None

        if audio_path and os.path.exists(audio_path):
            try:
                audio = AudioFileClip(audio_path)
                audio_duration = audio.duration
            except Exception as e:
                self.logger.warning(f"Audio preload failed: {e}")

        # ==================================================
        # SCENE LOOP
        # ==================================================
        for i, scene in enumerate(scenes):

            try:
                self.logger.info(f"Processing scene {i + 1}")

                media = scene.get("media")
                text = scene.get("text", "")

                # FIX: smooth pacing without cutting narration
                duration = float(scene.get("duration_seconds", 4))
                duration = max(2.5, min(duration + 0.6, 15))

                clip = self._create_clip(media, duration)

                if not clip:
                    continue

                # effects (safe wrapper)
                try:
                    clip = effects_service.apply_effects(clip)
                except Exception as e:
                    self.logger.warning(f"Effects failed: {e}")

                # text overlay (FULL SYSTEM RESTORED)
                clip = self._add_text_overlay(clip, text)

                clips.append(clip)

            except Exception as e:
                self.logger.error(f"Scene failed: {e}")

        if not clips:
            raise Exception("No clips generated")

        # ==================================================
        # CONCATENATION
        # ==================================================
        final_video = concatenate_videoclips(clips, method="compose")

        # ==================================================
        # AUDIO SYNC FIX
        # ==================================================
        if audio:

            try:
                final_duration = min(final_video.duration, audio_duration)

                final_video = final_video.subclip(0, final_duration)
                audio = audio.subclip(0, final_duration)

                final_video = final_video.set_audio(audio)

            except Exception as e:
                self.logger.warning(f"Audio sync failed: {e}")

        # ==================================================
        # EXPORT (OPTIMIZED BUT HIGH QUALITY)
        # ==================================================
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                preset="medium",   # balance quality + speed
                threads=4,
                logger=None
            )

        finally:
            try:
                final_video.close()
            except:
                pass

            for c in clips:
                try:
                    c.close()
                except:
                    pass

        self.logger.info(f"Video built successfully: {output_path}")
        return output_path

    # ==================================================
    # CREATE CLIP
    # ==================================================
    def _create_clip(self, media: dict, duration: int):

        if not media or not media.get("url"):
            return self._fallback_clip(duration)

        try:
            url = media["url"]
            media_type = media.get("type", "image")

            path = self._download_media(url, media_type)

            if not path:
                return self._fallback_clip(duration)

            # VIDEO
            if media_type == "video":

                clip = VideoFileClip(path, audio=False)

                usable = min(duration, clip.duration)
                clip = clip.subclip(0, usable)

                return self._resize(clip)

            # IMAGE
            return self._resize(
                ImageClip(path).set_duration(duration)
            )

        except Exception as e:
            self.logger.error(f"Clip error: {e}")
            return self._fallback_clip(duration)

    # ==================================================
    # DOWNLOAD (FIXED FOR INCOMPLETE READ)
    # ==================================================
    def _download_media(self, url, media_type):

        try:
            if not url:
                return None

            if not url.startswith("http"):
                return url

            ext = ".mp4" if media_type == "video" else ".jpg"

            file_path = os.path.join(self.temp_dir, f"{uuid.uuid4()}{ext}")

            # FIX: retry-safe download
            for attempt in range(2):

                try:
                    response = requests.get(url, timeout=30, stream=True)

                    if response.status_code != 200:
                        continue

                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(8192):
                            if chunk:
                                f.write(chunk)

                    if os.path.getsize(file_path) > 2000:
                        return file_path

                except Exception:
                    continue

            return None

        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return None

    # ==================================================
    # RESIZE
    # ==================================================
    def _resize(self, clip):

        try:
            return clip.resize(height=1920).set_position("center")
        except:
            return clip

    # ==================================================
    # TEXT OVERLAY (FULL RESTORED VERSION)
    # ==================================================
    def _add_text_overlay(self, clip, text):

        if not text:
            return clip

        try:
            text = text[:100]

            width, height = 1000, 260

            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 58)
            except:
                font = ImageFont.load_default()

            words = text.split()
            lines, current = [], ""

            for word in words:
                test = (current + " " + word).strip()

                bbox = draw.textbbox((0, 0), test, font=font)
                if (bbox[2] - bbox[0]) <= 850:
                    current = test
                else:
                    lines.append(current)
                    current = word

            if current:
                lines.append(current)

            y = 20

            for line in lines:

                bbox = draw.textbbox((0, 0), line, font=font)
                x = (width - (bbox[2] - bbox[0])) // 2

                # stroke (RESTORED FULL EFFECT)
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        draw.text((x + dx, y + dy), line, font=font, fill="black")

                draw.text((x, y), line, font=font, fill="white")

                y += 70

            txt_clip = (
                ImageClip(np.array(img))
                .set_duration(clip.duration)
                .set_position(("center", 1480))
            )

            return CompositeVideoClip([clip, txt_clip])

        except Exception as e:
            self.logger.warning(f"Text overlay failed: {e}")
            return clip

    # ==================================================
    # FALLBACK
    # ==================================================
    def _fallback_clip(self, duration):
        return ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(duration)


# ==================================================
# SINGLETON
# ==================================================
video_builder_service = VideoBuilderService()