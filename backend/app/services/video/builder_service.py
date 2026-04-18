import os
from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip
)

from app.core.logger import logger
from app.services.video.effects_service import effects_service


class VideoBuilderService:
    """
    Builds final video from scenes + audio + media
    """

    def __init__(self):
        self.logger = logger

    def build_video(self, scenes: list, audio_path: str, output_path: str):

        self.logger.info("Starting video build process")

        clips = []

        for scene in scenes:

            media = scene.get("media")
            duration = scene.get("duration", 3)
            text = scene.get("text", "")

            clip = self._create_clip(media, duration)

            # Apply effects (zoom, fade, etc.)
            clip = effects_service.apply_effects(clip)

            # Add text overlay
            clip = self._add_text_overlay(clip, text)

            clips.append(clip)

        # Merge all clips
        final_video = concatenate_videoclips(clips, method="compose")

        # Add audio
        audio = AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio)

        # Export
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac"
        )

        self.logger.info(f"Video built successfully: {output_path}")

        return output_path

    def _create_clip(self, media: dict, duration: int):

        if not media or not media.get("url"):
            return ImageClip("placeholder.jpg").set_duration(duration)

        if media["type"] == "video":
            return VideoFileClip(media["url"]).subclip(0, duration)

        return ImageClip(media["url"]).set_duration(duration)

    def _add_text_overlay(self, clip, text: str):

        txt = TextClip(
            text,
            fontsize=60,
            color="white",
            method="caption",
            size=clip.size
        ).set_duration(clip.duration)

        return CompositeVideoClip([clip, txt.set_position("center")])


video_builder_service = VideoBuilderService()