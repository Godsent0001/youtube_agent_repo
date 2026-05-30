from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from typing import List, Optional
from app.schemas.video import VideoCreate, VideoResponse, VideoListResponse, VideoGenerateRequest
from app.controllers.video_controller import video_controller
from app.routes.auth_routes import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("", response_model=VideoResponse)
async def create_video(video: VideoCreate):
    return await video_controller.create_video(video)

@router.get("", response_model=List[VideoResponse])
async def get_videos(user_id: str = Query(...)):
    return await video_controller.get_user_videos(user_id)

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    return await video_controller.get_video(video_id)

@router.post("/generate")
async def generate_video(
    request: VideoGenerateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Start the autonomous video generation pipeline
    """
    return await video_controller.generate_video_prompt(
        user_id=str(current_user.id),
        prompt=request.prompt,
        content_type=request.content_type,
        video_length=request.video_length,
        background_tasks=background_tasks
    )
