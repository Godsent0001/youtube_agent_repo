from typing import List, Optional
from app.db.session import db
from app.models.video import Video
from app.schemas.video import VideoCreate
from bson import ObjectId
from app.services.pipeline_service import pipeline_service
from app.queue.redis_queue import video_queue
from fastapi import BackgroundTasks
import uuid

class VideoController:
    async def create_video(self, video_data: VideoCreate):
        video_dict = video_data.model_dump()
        video_dict["created_at"] = video_dict.get("created_at") or video_data.created_at
        result = await db["videos"].insert_one(video_dict)
        video_dict["id"] = str(result.inserted_id)
        return video_dict

    async def get_user_videos(self, user_id: str) -> List[dict]:
        cursor = db["videos"].find({"user_id": user_id}).sort("created_at", -1)
        videos = await cursor.to_list(length=100)
        for v in videos:
            v["id"] = str(v["_id"])
        return videos

    async def get_video(self, video_id: str) -> Optional[dict]:
        video = await db["videos"].find_one({"_id": ObjectId(video_id)})
        if video:
            video["id"] = str(video["_id"])
        return video

    async def generate_video_prompt(self, user_id: str, prompt: str, content_type: str, video_length: int, background_tasks: BackgroundTasks):
        """
        Enqueues a background job to generate a video from a prompt
        """
        # Create a job record in MongoDB first to track it
        job_id = str(uuid.uuid4())

        from app.services.video_jobs import create_video_job
        create_video_job(job_id, user_id, "MorphFlow Generation")

        # Enqueue to Redis Queue
        # We use background_tasks as a fallback or if Redis is not configured,
        # but the primary way is via the video_queue
        video_queue.enqueue(
            pipeline_service.run,
            args=(user_id, prompt, content_type, video_length, job_id),
            job_id=job_id,
            job_timeout=3600,
            timeout=3600
        )

        return {"job_id": job_id, "status": "queued"}

video_controller = VideoController()
