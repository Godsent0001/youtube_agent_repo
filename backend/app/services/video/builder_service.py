import os
import requests
import uuid
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

# Monkey patch moviepy's resize effect to fix Pillow ANTIALIAS issue
import moviepy.video.fx.resize as resize
from PIL import Image

if not hasattr(Image, 'ANTIALIAS'):
    # Resampling filters were moved to Image.Resampling in Pillow 10+
    if hasattr(Image, 'Resampling'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    else:
        Image.ANTIALIAS = Image.BICUBIC # Fallback

class VideoBuilderService:
    """
    Builds final video from scenes + audio + media
    """

    def __init__(self):
        self.logger = logger
        self.temp_dir = "storage/temp_media"
        os.makedirs(self.temp_dir, exist_ok=True)

    def build_video(self, scenes: list, audio_path: str, output_path: str):

        self.logger.info("Starting video build process")

        clips = []

        for scene in scenes:

            media = scene.get("media")
            duration = scene.get("duration", 5) or scene.get("duration_seconds", 5)
            text = scene.get("text", "")

            clip = self._create_clip(media, duration)
            if not clip:
                continue

            # Apply effects (zoom, fade, etc.)
            try:
                clip = effects_service.apply_effects(clip)
            except Exception as ee:
                self.logger.warning(f"Failed to apply effects: {ee}")

            # Add text overlay (TextClip might fail if ImageMagick is not installed)
            # clip = self._add_text_overlay(clip, text)

            clips.append(clip)

        if not clips:
            raise Exception("No clips generated for video build")

        # Merge all clips
        final_video = concatenate_videoclips(clips, method="compose")

        # Add audio
        if os.path.exists(audio_path):
            try:
                audio = AudioFileClip(audio_path)
                final_video = final_video.set_audio(audio)
            except Exception as ae:
                self.logger.warning(f"Failed to add audio: {ae}")

        # Export
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac"
            )
        except Exception as ve:
            self.logger.error(f"Failed to export video: {ve}")
            raise ve

        self.logger.info(f"Video built successfully: {output_path}")

        return output_path

    def _create_clip(self, media: dict, duration: int):

        if not media or not media.get("url"):
            return ColorClip(size=(1280, 720), color=(0, 0, 0)).set_duration(duration)

        try:
            # Download media if it's a URL
            media_url = media["url"]
            if media_url.startswith("http"):
                ext = ".mp4" if media["type"] == "video" else ".jpg"
                local_path = os.path.join(self.temp_dir, f"{uuid.uuid4()}{ext}")
                response = requests.get(media_url, timeout=30)
                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    media_path = local_path
                else:
                    self.logger.error(f"Failed to download media: {media_url}")
                    return ColorClip(size=(1280, 720), color=(0, 0, 0)).set_duration(duration)
            else:
                media_path = media_url

            if media["type"] == "video":
                # Ensure the file exists and is not empty before loading
                if os.path.exists(media_path) and os.path.getsize(media_path) > 0:
                    return VideoFileClip(media_path).subclip(0, min(duration, 10))
                else:
                    return ColorClip(size=(1280, 720), color=(0, 0, 0)).set_duration(duration)

            return ImageClip(media_path).set_duration(duration)
        except Exception as e:
            self.logger.error(f"Error creating clip: {e}")
            return ColorClip(size=(1280, 720), color=(0, 0, 0)).set_duration(duration)

    def _add_text_overlay(self, clip, text: str):
        # Skipping TextClip for now to avoid ImageMagick dependency issues in this environment
        return clip


video_builder_service = VideoBuilderService()
