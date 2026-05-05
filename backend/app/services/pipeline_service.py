from app.core.logger import logger

from app.services.ai.topic_service import topic_service
from app.services.ai.research_service import research_service
from app.services.ai.script_service import script_service
from app.services.ai.metadata_service import metadata_service
from app.services.ai.scene_service import scene_service

from app.services.media.selector_service import selector_service
from app.services.media.thumbnail_service import ThumbnailService

from app.services.audio.elevenlabs_service import elevenlabs_service

from app.services.video.builder_service import video_builder_service
from app.services.video.render_service import RenderService
from app.services.video.subtitle_service import subtitle_service

from app.services.youtube.youtube_service import youtube_service


class PipelineService:
    """
    FULL autonomous AI video generation pipeline
    """

    def __init__(self):
        self.logger = logger
        self.render_service = RenderService()
        self.thumbnail_service = ThumbnailService()

    def run(self, agent: dict):

        self.logger.info(f"Pipeline started for agent: {agent['name']}")

        # =========================
        # 1. TOPIC GENERATION
        # =========================
        topic_data = topic_service.generate_topic(
            niche=agent["niche"],
            content_type=agent["content_type"],
            custom_prompt=agent.get("custom_prompt")
        )

        topic = topic_data["topic"]

        # =========================
        # 2. RESEARCH
        # =========================
        research = research_service.generate_research(
            topic=topic,
            niche=agent["niche"]
        )

        # =========================
        # 3. SCRIPT
        # =========================
        script_data = script_service.generate_script(
            topic=topic,
            niche=agent["niche"],
            content_type=agent["content_type"],
            research=research
        )

        script = script_data["script"]

        # =========================
        # 4. SCENES
        # =========================
        scenes = scene_service.generate_scenes(
            script=script,
            content_type=agent["content_type"]
        )

        # =========================
        # 5. MEDIA ATTACHMENT
        # =========================
        for scene in scenes:
            scene["media"] = selector_service.get_best_media(scene)

        # =========================
        # 6. AUDIO GENERATION
        # =========================
        audio_path = elevenlabs_service.generate_audio(script)

        # =========================
        # 7. METADATA
        # =========================
        metadata = metadata_service.generate_metadata(
            topic=topic,
            script=script,
            niche=agent["niche"]
        )

        # =========================
        # 8. THUMBNAIL
        # =========================
        thumbnail_path = self.thumbnail_service.generate_thumbnail(
            title=metadata["title"],
            script=script,
            niche=agent["niche"]
        )

        # =========================
        # 9. BUILD VIDEO
        # =========================
        raw_video_path = video_builder_service.build_video(
            scenes=scenes,
            audio_path=audio_path,
            output_path=f"storage/videos/raw_{agent['_id']}.mp4"
        )

        # =========================
        # 10. RENDER FINAL VIDEO
        # =========================
        final_video = self.render_service.render_final_video(
            clips=[raw_video_path],
            output_path=f"storage/videos/final_{agent['_id']}.mp4",
            content_type=agent["content_type"]
        )

        # =========================
        # 11. UPLOAD TO YOUTUBE
        # =========================
        upload_result = youtube_service.upload_video(
            user_id=agent["user_id"],
            file_path=final_video,
            title=metadata["title"],
            description=metadata["description"],
            tags=metadata["tags"],
            thumbnail_path=thumbnail_path,
            content_type=agent["content_type"]
        )

        self.logger.info("Pipeline completed successfully")

        return upload_result


pipeline_service = PipelineService()