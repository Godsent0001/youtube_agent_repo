import os

from app.core.logger import logger

from app.services.ai.topic_service import topic_service
from app.services.ai.research_service import research_service
from app.services.ai.script_service import script_service
from app.services.ai.metadata_service import metadata_service
from app.services.ai.scene_service import scene_service
from datetime import datetime

from app.services.media.selector_service import selector_service
from app.services.media.thumbnail_service import ThumbnailService

from app.services.audio.elevenlabs_service import elevenlabs_service

from app.services.video.builder_service import video_builder_service
from app.services.video.render_service import RenderService
from app.services.video.subtitle_service import subtitle_service


class PipelineService:
    """
    FULL autonomous AI video generation pipeline
    """

    def __init__(self):
        self.logger = logger
        self.render_service = RenderService()
        self.thumbnail_service = ThumbnailService()

    def run(self, user_id: str, custom_prompt: str, content_type: str, video_length: int, job_id: str = None):

        from app.services.video_jobs import update_job_activity

        self.logger.info(
            f"Pipeline started for user: {user_id} with prompt: {custom_prompt}"
        )

        # Create folders
        os.makedirs("storage/videos", exist_ok=True)

        # =========================
        # 1. TOPIC GENERATION
        # =========================
        self.logger.info("Generating topic...")
        if job_id:
            update_job_activity(job_id, "Generating topic...", progress=5)

        topic_data = topic_service.generate_topic(
            niche="", # Niche is now derived from prompt
            content_type=content_type,
            custom_prompt=custom_prompt
        )

        topic = topic_data.get("topic")

        if not topic:
            raise Exception("Topic generation failed")

        self.logger.info(f"Topic generated: {topic}")

        # =========================
        # 2. RESEARCH
        # =========================
        self.logger.info("Generating research...")
        if job_id:
            update_job_activity(job_id, "Generating research...", progress=10)

        research = research_service.generate_research(
            topic=topic,
            niche=""
        )

        # =========================
        # 3. SCRIPT
        # =========================
        self.logger.info("Generating script...")
        if job_id:
            update_job_activity(job_id, "Generating script...", progress=15)

        script_data = script_service.generate_script(
            topic=topic,
            niche="",
            content_type=content_type,
            research=research,
            video_length=video_length,
            custom_prompt=custom_prompt
        )

        script = script_data.get("script")

        if not script:
            raise Exception("Script generation failed")

        # =========================
        # 4. SCENES
        # =========================
        self.logger.info("Generating scenes...")
        if job_id:
            update_job_activity(job_id, "Generating scenes...", progress=20)

        scenes = scene_service.generate_scenes(
            script=script,
            content_type=content_type,
            video_length=video_length
        )

        if not scenes:
            raise Exception("Scene generation failed")

        # =========================
        # 5. MEDIA ATTACHMENT
        # =========================
        self.logger.info("Attaching media to scenes...")
        if job_id:
            update_job_activity(job_id, "Selecting best media for scenes...", progress=25)

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
        if job_id:
            update_job_activity(job_id, "Downloading media files...", progress=30)
        video_builder_service.prefetch_media(scenes)

        # =========================
        # 7. AUDIO GENERATION (SYNCED WITH SCENES)
        # =========================
        self.logger.info("Generating audio...")
        if job_id:
            update_job_activity(job_id, "Generating AI voiceover...", progress=40)

        # FIX: ensure audio script matches exactly what's in scenes
        # this prevents "hanging" narration at the end of the video
        scene_scripts = [s.get("text", "") for s in scenes if s.get("text")]
        synced_script = " ".join(scene_scripts)

        audio_path = elevenlabs_service.generate_audio(synced_script or script)

        if not audio_path:
            raise Exception("Audio generation failed")

        self.logger.info(f"Audio generated: {audio_path}")

        # =========================
        # 8. BUILD VIDEO (INTEGRATED)
        # =========================
        self.logger.info("Building and rendering video...")
        if job_id:
            update_job_activity(job_id, "Rendering final video...", progress=50)

        import uuid
        video_uuid = str(uuid.uuid4())
        final_video_filename = f"final_{video_uuid}.mp4"
        final_video_path = f"storage/videos/{final_video_filename}"

        final_video = video_builder_service.build_video(
            scenes=scenes,
            audio_path=audio_path,
            output_path=final_video_path,
            content_type=content_type,
            video_length=video_length,
            job_id=job_id
        )

        if not final_video:
            raise Exception("Final video generation failed")

        self.logger.info(
            f"Final video created: {final_video}"
        )

        # =========================
        # 9. SAVE TO DATABASE
        # =========================
        from app.db.session import db

        video_record = {
            "user_id": user_id,
            "content_type": content_type,
            "topic": topic,
            "script": script,
            "scenes": scenes,
            "video_url": f"/storage/videos/{final_video_filename}",
            "status": "completed",
            "created_at": datetime.utcnow()
        }
        db["videos"].insert_one(video_record)

        self.logger.info(
            "Pipeline completed successfully"
        )

        return {
            "success": True,
            "topic": topic,
            "audio_path": audio_path,
            "final_video_path": final_video
        }


pipeline_service = PipelineService()
