from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from typing import List
import os

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services.agent_service import agent_service
from app.queue.redis_queue import video_queue
from app.services.video_jobs import generate_video_job
from app.db.session import db
from datetime import datetime
from app.core.config import settings
from app.core.logger import logger
from app.queue.redis_queue import redis_conn
from google_auth_oauthlib.flow import Flow
import secrets

router = APIRouter(prefix="/agents", tags=["Agents"])

# Allow insecure transport for local development (if DEBUG=True)
if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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
        agent_id,
        custom_job_id,
        job_timeout=3600
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
# YOUTUBE OAUTH CONNECT
# =========================
@router.get("/{agent_id}/youtube/connect")
def connect_youtube(agent_id: str, request: Request):
    """
    Starts the OAuth flow for a specific agent
    """
    logger.info(f"Initiating YouTube OAuth for agent: {agent_id}")

    if not settings.YOUTUBE_CLIENT_ID or not settings.YOUTUBE_CLIENT_SECRET:
        logger.error("YouTube credentials missing in settings")
        raise HTTPException(status_code=500, detail="YouTube service not configured")

    client_config = {
        "web": {
            "client_id": settings.YOUTUBE_CLIENT_ID,
            "client_secret": settings.YOUTUBE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # Use explicit BACKEND_URL for redirect URI
    base_url = settings.BACKEND_URL.rstrip('/')
    flow.redirect_uri = f"{base_url}/agents/youtube/callback"
    logger.info(f"OAuth redirect URI: {flow.redirect_uri}")

    # Secure state management with Redis
    state_token = secrets.token_urlsafe(32)
    if redis_conn:
        redis_conn.setex(f"oauth_state:{state_token}", 600, agent_id)
    else:
        logger.warning("Redis not available, falling back to insecure state")
        # In case Redis is down, we could potentially fallback but for now we follow the rule
        # If Redis is strictly required for security, we should fail here.
        # But let's assume it's available in production.
        raise HTTPException(status_code=503, detail="Redis service unavailable for secure OAuth")

    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent', # Force consent screen to ensure refresh token is returned
        state=state_token
    )

    return RedirectResponse(authorization_url, status_code=302)


# =========================
# YOUTUBE OAUTH CALLBACK
# =========================
@router.get("/youtube/callback")
def youtube_callback(request: Request, state: str, code: str):
    """
    Handles the redirect from Google
    """
    # Validate state using Redis
    if not redis_conn:
        logger.error("Redis connection lost during OAuth callback")
        raise HTTPException(status_code=500, detail="Redis connection lost")

    agent_id_bytes = redis_conn.get(f"oauth_state:{state}")
    if not agent_id_bytes:
        logger.error(f"Invalid or expired OAuth state: {state}")
        raise HTTPException(status_code=400, detail="Invalid or expired OAuth state")

    agent_id = agent_id_bytes.decode('utf-8')
    logger.info(f"Received YouTube OAuth callback for agent: {agent_id}")

    client_config = {
        "web": {
            "client_id": settings.YOUTUBE_CLIENT_ID,
            "client_secret": settings.YOUTUBE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    base_url = settings.BACKEND_URL.rstrip('/')
    flow.redirect_uri = f"{base_url}/agents/youtube/callback"

    try:
        flow.fetch_token(code=code)
    except Exception as e:
        logger.error("Failed to fetch YouTube token")
        # Redirect back with error or to a safe place
        return RedirectResponse(f"{settings.FRONTEND_URL}/agent/{agent_id}?error=oauth_failed")

    creds = flow.credentials

    # Update agent with tokens
    agent_service.update_agent(agent_id, {
        "youtube_access_token": creds.token,
        "youtube_refresh_token": creds.refresh_token,
        "youtube_token_expiry": creds.expiry
    })

    logger.info(f"YouTube tokens stored successfully for agent: {agent_id}")

    # Redirect back to frontend agent detail page
    return RedirectResponse(f"{settings.FRONTEND_URL}/agent/{agent_id}")


# =========================
# DELETE AGENT
# =========================
@router.delete("/{agent_id}")
def delete_agent(agent_id: str):

    success = agent_service.delete_agent(agent_id)

    if not success:
        raise HTTPException(status_code=404, detail="Agent not found or could not be deleted")

    return {"message": "Agent deleted successfully"}