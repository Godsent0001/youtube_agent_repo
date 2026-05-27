from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from typing import List
import os

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services.agent_service import agent_service
from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job, on_video_job_failure
from app.db.session import db
from datetime import datetime
from app.core.config import settings
from app.core.logger import logger
router = APIRouter(prefix="/agents", tags=["Agents"])


# =========================
# CREATE AGENT
# =========================
@router.post("", response_model=str)
def create_agent(payload: AgentCreate, user_id: str):

    agent_id = agent_service.create_agent(
        user_id=user_id,
        data=payload.dict()
    )

    return agent_id


# =========================
# GET ALL USER AGENTS
# =========================
@router.get("", response_model=List[dict])
def get_agents(user_id: str):

    return agent_service.list_user_agents(user_id)


# =========================
# GET SINGLE AGENT
# =========================
@router.get("/{agent_id}")
def get_agent(agent_id: str):

    agent = agent_service.get_agent(agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


# =========================
# UPDATE AGENT
# =========================
@router.put("/{agent_id}")
def update_agent(agent_id: str, payload: AgentUpdate):

    updated = agent_service.update_agent(
        agent_id,
        payload.dict(exclude_unset=True)
    )

    return updated


# =========================
# TRIGGER VIDEO GENERATION
# =========================
@router.post("/{agent_id}/generate")
def generate_video(agent_id: str):

    """
    THIS is the most important endpoint:
    pushes job into Redis worker queue and records in MongoDB
    """
    from bson import ObjectId

    # Atomic check and update to prevent duplicate generation
    # Also handle cases where status might be missing (treat as idle)
    agent = db["agents"].find_one_and_update(
        {
            "_id": ObjectId(agent_id),
            "status": {"$in": ["idle", "failed", None]}
        },
        {
            "$set": {
                "status": "queued",
                "is_active": True,
                "last_queued_at": datetime.utcnow()
            }
        },
        return_document=True
    )

    if not agent:
        # Check if agent exists at all
        existing = db["agents"].find_one({"_id": ObjectId(agent_id)})
        if not existing:
            raise HTTPException(status_code=404, detail="Agent not found")

        # If it exists but isn't idle
        current_status = existing.get('status', 'unknown')
        logger.warning(f"Generation attempt for agent {agent_id} failed because status is {current_status}")
        raise HTTPException(
            status_code=409,
            detail=f"Agent is already {current_status}. Please wait."
        )

    if not video_queue:
        # Reset status if queue is down
        db["agents"].update_one(
            {"_id": ObjectId(agent_id)},
            {"$set": {"status": "idle"}}
        )
        raise HTTPException(status_code=503, detail="Redis queue not available")

    # 1. Enqueue job with POSITIONAL arguments
    user_id = agent.get("user_id")
    import uuid
    custom_job_id = str(uuid.uuid4())

    new_job = video_queue.enqueue(
        generate_video_job,
        args=(agent_id, custom_job_id),
        job_timeout=3600,
        on_failure=on_video_job_failure
    )

    # 3. Create job record in MongoDB
    db["jobs"].insert_one({
        "job_id": custom_job_id,
        "rq_job_id": new_job.id,
        "user_id": user_id,
        "agent_id": agent_id,
        "status": "queued",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "result_url": None,
        "error": None
    })

    return {
        "message": "Video generation started and agent activated",
        "agent_id": agent_id,
        "job_id": custom_job_id
    }




# =========================
# DELETE AGENT
# =========================
@router.delete("/{agent_id}")
def delete_agent(agent_id: str):

    success = agent_service.delete_agent(agent_id)

    if not success:
        raise HTTPException(status_code=404, detail="Agent not found or could not be deleted")

    return {"message": "Agent deleted successfully"}