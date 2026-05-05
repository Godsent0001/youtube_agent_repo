import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from app.core.logger import logger


class RenderService:
    """
    Final video rendering layer
    Handles export optimization for YouTube
    """

    def __init__(self):
        self.logger = logger

    def render_final_video(
        self,
        clips: list,
        output_path: str,
        content_type: str = "shorts"
    ):

        self.logger.info(f"Rendering final video... (Input: {clips})")

        # 1. Validate input
        if not clips:
            raise ValueError("No clips provided for rendering")

        # 2. Convert string paths to VideoFileClip objects if necessary
        processed_clips = []
        for c in clips:
            if isinstance(c, str):
                if os.path.exists(c):
                    processed_clips.append(VideoFileClip(c))
                else:
                    self.logger.error(f"Clip file not found: {c}")
            else:
                processed_clips.append(c)

        if not processed_clips:
             raise ValueError("No valid clips found for rendering")

        # 3. Composition strategy
        final_clip = self._compose(processed_clips, content_type)

        # 4. Export settings
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        fps = 30 if content_type == "shorts" else 24

        final_clip.write_videofile(
            output_path,
            fps=fps,
            codec="libx264",
            audio_codec="aac",
            bitrate="2500k",
            threads=4
        )

        self.logger.info(f"Render complete: {output_path}")

        return output_path

    def _compose(self, clips, content_type):

        """
        Handles composition logic
        """

        if content_type == "shorts":
            # vertical-first assumption (9:16)
            return concatenate_videoclips(clips, method="compose")

        # long form: allow layered composition later
        return CompositeVideoClip(clips)
