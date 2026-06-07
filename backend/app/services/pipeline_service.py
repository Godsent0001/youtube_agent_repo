import os
from datetime import datetime
from app.core.logger import logger

from app.services.ai.script_service import script_service
from app.services.ai.metadata_service import metadata_service
from app.services.ai.scene_service import scene_service

from app.services.media.selector_service import selector_service
from app.services.audio.piper_service import piper_service

from app.services.video.builder_service import video_builder_service
from app.services.video.render_service import RenderService


class PipelineService:
    """
    MorphFlow AI video generation pipeline
    """

    def __init__(self):
        self.logger = logger
        self.render_service = RenderService()

    def run(self, video: dict, job_id: str = None):
        from app.services.video_jobs import update_job_activity

        video_id = str(video.get("id"))
        user_id = video.get("user_id")
        prompt = video.get("prompt")
        aspect_ratio = video.get("aspect_ratio", "16:9")
        duration_seconds = video.get("duration_seconds", 30)

        edit_prompt = video.get("edit_prompt")
        original_video_id = video.get("original_video_id")

        self.logger.info(f"Pipeline started for video: {video_id} (User: {user_id})")

        # Create folders
        os.makedirs("storage/videos", exist_ok=True)
        os.makedirs("storage/audio", exist_ok=True)
        os.makedirs("storage/images", exist_ok=True)

        # =========================
        # 1. SCRIPT GENERATION
        # =========================
        self.logger.info("Generating script...")
        if job_id:
            update_job_activity(job_id, "Generating script...", progress=10)

        # For regeneration/edit, we might want to pass more context
        context = ""
        if edit_prompt and original_video_id:
             # In a real scenario, we'd fetch the original script/scenes here
             # For now, let's just combine the prompts
             full_prompt = f"Original vision: {prompt}\n\nEdit instruction: {edit_prompt}"
        else:
             full_prompt = prompt

        script_data = script_service.generate_script(
            topic=full_prompt, # Use prompt as topic context
            niche="General",
            content_type="shorts" if aspect_ratio == "9:16" else "long",
            video_length=f"{duration_seconds}s"
        )

        script = script_data.get("script")
        if not script:
            raise Exception("Script generation failed")

        # =========================
        # 2. SCENE GENERATION
        # =========================
        self.logger.info("Generating scenes...")
        if job_id:
            update_job_activity(job_id, "Generating scenes...", progress=20)

        scenes = scene_service.generate_scenes(
            script=script,
            content_type="shorts" if aspect_ratio == "9:16" else "long",
            video_length=f"{duration_seconds}s"
        )

        if not scenes:
            raise Exception("Scene generation failed")

        # =========================
        # 3. MEDIA ATTACHMENT
        # =========================
        self.logger.info("Attaching media to scenes...")
        if job_id:
            update_job_activity(job_id, "Selecting best media for scenes...", progress=30)

        for scene in scenes:
            try:
                scene["media"] = selector_service.get_best_media(scene)
            except Exception as media_error:
                self.logger.error(f"Media selection failed: {media_error}")
                scene["media"] = None

        # =========================
        # 4. PRE-DOWNLOAD MEDIA
        # =========================
        self.logger.info("Pre-downloading media...")
        if job_id:
            update_job_activity(job_id, "Downloading media files...", progress=40)
        video_builder_service.prefetch_media(scenes)

        # =========================
        # 5. AUDIO GENERATION
        # =========================
        self.logger.info("Generating audio...")
        if job_id:
            update_job_activity(job_id, "Generating AI voiceover...", progress=50)

        scene_scripts = [s.get("text", "") for s in scenes if s.get("text")]
        synced_script = " ".join(scene_scripts)

        audio_path = piper_service.generate_audio(synced_script or script)
        if not audio_path:
            raise Exception("Audio generation failed")

        # =========================
        # 6. METADATA (TITLE/DESCRIPTION)
        # =========================
        self.logger.info("Generating metadata...")
        metadata = metadata_service.generate_metadata(
            topic=prompt,
            script=script,
            niche="General"
        )
        title = metadata.get("title", "MorphFlow Video")
        description = metadata.get("description", "")

        from app.db.session import videos_collection
        from bson import ObjectId
        videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"title": title, "description": description, "script": script}}
        )

        # =========================
        # 7. BUILD VIDEO
        # =========================
        self.logger.info("Building and rendering video...")
        if job_id:
            update_job_activity(job_id, "Rendering final video...", progress=60)

        output_filename = f"final_{video_id}_{int(datetime.utcnow().timestamp())}.mp4"
        final_video = video_builder_service.build_video(
            scenes=scenes,
            audio_path=audio_path,
            output_path=f"storage/videos/{output_filename}",
            content_type="shorts" if aspect_ratio == "9:16" else "long",
            video_length=f"{duration_seconds}s",
            job_id=job_id
        )

        if not final_video:
            raise Exception("Final video generation failed")

        self.logger.info(f"Final video created: {final_video}")
        if job_id:
            update_job_activity(job_id, "Video ready!", progress=100)

        return {
            "success": True,
            "video_id": video_id,
            "title": title,
            "final_video_path": final_video,
            "thumbnail_url": None # Could be extracted from video if needed
        }


pipeline_service = PipelineService()
