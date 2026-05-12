import os

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

        # =========================
        # SAFE AGENT ACCESS
        # =========================
        agent_id = str(
            agent.get("_id") or agent.get("id") or "unknown_agent"
        )

        agent_name = agent.get("name", "Unnamed Agent")

        user_id = agent.get("user_id")

        if not user_id:
            raise Exception("Agent missing user_id")

        self.logger.info(
            f"Pipeline started for agent: {agent_name}"
        )

        # Create folders
        os.makedirs("storage/videos", exist_ok=True)

        # =========================
        # 1. TOPIC GENERATION
        # =========================
        self.logger.info("Generating topic...")

        topic_data = topic_service.generate_topic(
            niche=agent.get("niche", ""),
            content_type=agent.get("content_type", "youtube"),
            custom_prompt=agent.get("custom_prompt")
        )

        topic = topic_data.get("topic")

        if not topic:
            raise Exception("Topic generation failed")

        self.logger.info(f"Topic generated: {topic}")

        # =========================
        # 2. RESEARCH
        # =========================
        self.logger.info("Generating research...")

        research = research_service.generate_research(
            topic=topic,
            niche=agent.get("niche", "")
        )

        # =========================
        # 3. SCRIPT
        # =========================
        self.logger.info("Generating script...")

        script_data = script_service.generate_script(
            topic=topic,
            niche=agent.get("niche", ""),
            content_type=agent.get("content_type", "youtube"),
            research=research
        )

        script = script_data.get("script")

        if not script:
            raise Exception("Script generation failed")

        # =========================
        # 4. SCENES
        # =========================
        self.logger.info("Generating scenes...")

        scenes = scene_service.generate_scenes(
            script=script,
            content_type=agent.get("content_type", "youtube")
        )

        if not scenes:
            raise Exception("Scene generation failed")

        # =========================
        # 5. MEDIA ATTACHMENT
        # =========================
        self.logger.info("Attaching media to scenes...")

        for scene in scenes:
            try:
                scene["media"] = selector_service.get_best_media(scene)
            except Exception as media_error:
                self.logger.error(
                    f"Media selection failed: {media_error}"
                )
                scene["media"] = None

        # =========================
        # 6. PRE-DOWNLOAD MEDIA (SERIAL)
        # =========================
        self.logger.info("Pre-downloading media serially...")
        video_builder_service.prefetch_media(scenes)

        # =========================
        # 7. AUDIO GENERATION (SYNCED WITH SCENES)
        # =========================
        self.logger.info("Generating audio...")

        # FIX: ensure audio script matches exactly what's in scenes
        # this prevents "hanging" narration at the end of the video
        scene_scripts = [s.get("text", "") for s in scenes if s.get("text")]
        synced_script = " ".join(scene_scripts)

        audio_path = elevenlabs_service.generate_audio(synced_script or script)

        if not audio_path:
            raise Exception("Audio generation failed")

        self.logger.info(f"Audio generated: {audio_path}")

        # =========================
        # 8. METADATA
        # =========================
        self.logger.info("Generating metadata...")

        metadata = metadata_service.generate_metadata(
            topic=topic,
            script=script,
            niche=agent.get("niche", "")
        )

        title = metadata.get("title", topic)
        description = metadata.get("description", "")
        tags = metadata.get("tags", [])

        # =========================
        # 9. THUMBNAIL
        # =========================
        self.logger.info("Generating thumbnail...")

        thumbnail_path = self.thumbnail_service.generate_thumbnail(
            title=title,
            script=script,
            niche=agent.get("niche", "")
        )

        self.logger.info(
            f"Thumbnail generated successfully: {thumbnail_path}"
        )

        # =========================
        # 10. BUILD VIDEO (INTEGRATED)
        # =========================
        self.logger.info("Building and rendering video...")

        final_video = video_builder_service.build_video(
            scenes=scenes,
            audio_path=audio_path,
            output_path=f"storage/videos/final_{agent_id}.mp4",
            content_type=agent.get("content_type", "shorts")
        )

        if not final_video:
            raise Exception("Final video generation failed")

        self.logger.info(
            f"Final video created: {final_video}"
        )

        # =========================
        # 11. UPLOAD TO YOUTUBE
        # =========================
        self.logger.info("Uploading video to YouTube...")

        upload_result = youtube_service.upload_video(
            user_id=user_id,
            file_path=final_video,
            title=title,
            description=description,
            tags=tags,
            thumbnail_path=thumbnail_path,
            content_type=agent.get("content_type", "youtube")
        )

        self.logger.info(
            "Pipeline completed successfully"
        )

        return {
            "success": True,
            "agent_id": agent_id,
            "topic": topic,
            "title": title,
            "audio_path": audio_path,
            "thumbnail_path": thumbnail_path,
            "final_video_path": final_video,
            "youtube_upload": upload_result
        }


pipeline_service = PipelineService()
