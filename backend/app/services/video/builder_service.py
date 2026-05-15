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

from tqdm import tqdm
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
    # PREFETCH MEDIA
    # ==================================================
    def prefetch_media(self, scenes: list):
        """
        Downloads all media serially to save memory
        """
        for scene in scenes:
            media = scene.get("media")
            if media and media.get("url"):
                local_path = self._download_media(media["url"], media.get("type", "image"))
                if local_path:
                    media["local_path"] = local_path

    # ==================================================
    # MAIN PIPELINE
    # ==================================================
    def build_video(self, scenes: list, audio_path: str, output_path: str, content_type: str = "youtube"):

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
        # DURATION CALCULATION (DYNAMIC PROPORTIONAL)
        # ==================================================
        # Calculate total characters in all scenes to distribute audio duration
        total_chars = sum(len(s.get("text", "")) for s in scenes)
        if total_chars == 0:
            total_chars = 1

        # ==================================================
        # SCENE LOOP
        # ==================================================
        for i, scene in tqdm(enumerate(scenes), total=len(scenes), desc="Building scenes"):

            try:
                self.logger.info(f"Processing scene {i + 1}")

                media = scene.get("media")
                text = scene.get("text", "")

                # FIX: Proportional duration based on text length and total audio duration
                if audio_duration:
                    char_ratio = len(text) / total_chars
                    duration = char_ratio * audio_duration
                else:
                    duration = float(scene.get("duration_seconds", 4))

                # Clamp duration to reasonable limits
                duration = max(1.5, duration)

                clip = self._create_clip(media, duration, content_type)

                if not clip:
                    continue

                # effects (safe wrapper)
                try:
                    clip = effects_service.apply_effects(clip)
                except Exception as e:
                    self.logger.warning(f"Effects failed: {e}")

                # text overlay (DISABLED TO SAVE MEMORY/SPEED)
                clip = self._add_text_overlay(clip, text)

                clips.append(clip)

            except Exception as e:
                self.logger.error(f"Scene failed: {e}")

        if not clips:
            if audio:
                audio.close()
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
                # Force video duration to match audio EXACTLY to prevent black screen
                final_video = final_video.set_duration(audio_duration)
                final_video = final_video.set_audio(audio)

            except Exception as e:
                self.logger.warning(f"Audio sync failed: {e}")

        # =========================
        # EXPORT (OPTIMIZED)
        # =========================
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        fps = 30 if content_type == "shorts" else 24

        try:
            final_video.write_videofile(
                output_path,
                fps=fps,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",   # EXTREME SPEED
                threads=4,
                logger="bar" # Enable MoviePy progress bar
            )

        finally:
            try:
                final_video.close()
            except:
                pass

            if audio:
                try:
                    audio.close()
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
    def _create_clip(self, media: dict, duration: int, content_type: str = "youtube"):

        if not media or (not media.get("url") and not media.get("local_path")):
            return self._fallback_clip(duration, content_type)

        try:
            media_type = media.get("type", "image")
            path = media.get("local_path")

            if not path:
                path = self._download_media(media["url"], media_type)

            if not path:
                return self._fallback_clip(duration, content_type)

            # VIDEO
            if media_type == "video":
                clip = VideoFileClip(path, audio=False)

                # Loop video if it's shorter than required duration
                if clip.duration < duration:
                    from moviepy.editor import vfx
                    clip = clip.fx(vfx.loop, duration=duration)
                else:
                    clip = clip.subclip(0, duration)

                return self._resize(clip, content_type)

            # IMAGE
            return self._resize(
                ImageClip(path).set_duration(duration),
                content_type
            )

        except Exception as e:
            self.logger.error(f"Clip error: {e}")
            return self._fallback_clip(duration, content_type)

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
    def _resize(self, clip, content_type="youtube"):

        try:
            target_w, target_h = (1080, 1920) if content_type == "shorts" else (1920, 1080)

            # Resize while maintaining aspect ratio
            w, h = clip.size
            ratio = max(target_w / w, target_h / h)
            new_w, new_h = int(w * ratio), int(h * ratio)

            clip = clip.resize(newsize=(new_w, new_h))

            # Crop to exact target size
            return clip.crop(
                x_center=new_w / 2,
                y_center=new_h / 2,
                width=target_w,
                height=target_h
            )
        except Exception as e:
            self.logger.warning(f"Resize failed: {e}")
            return clip

    # ==================================================
    # TEXT OVERLAY (DISABLED)
    # ==================================================
    def _add_text_overlay(self, clip, text):
        return clip

    # ==================================================
    # FALLBACK
    # ==================================================
    def _fallback_clip(self, duration, content_type="youtube"):
        size = (1080, 1920) if content_type == "shorts" else (1920, 1080)
        return ColorClip(size=size, color=(0, 0, 0)).set_duration(duration)


# ==================================================
# SINGLETON
# ==================================================
video_builder_service = VideoBuilderService()
