from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from typing import List
import os

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services.agent_service import agent_service
from app.workers.worker import worker
from app.core.config import settings
from google_auth_oauthlib.flow import Flow

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
    pushes job into worker queue and sets agent to active
    """

    # Ensure agent is active when starting manual generation
    agent_service.update_agent(agent_id, {"is_active": True})

    worker.add_job("generate_video", {
        "agent_id": agent_id
    })

    return {
        "message": "Video generation started and agent activated",
        "agent_id": agent_id
    }


# =========================
# YOUTUBE OAUTH CONNECT
# =========================
@router.get("/{agent_id}/youtube/connect")
def connect_youtube(agent_id: str, request: Request):
    """
    Starts the OAuth flow for a specific agent
    """
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

    # Redirect URI must be registered in Google Cloud Console
    # We use a generic callback that will handle the state
    base_url = str(request.base_url).rstrip('/')
    if not settings.DEBUG:
        base_url = base_url.replace("http://", "https://")
    flow.redirect_uri = f"{base_url}/agents/youtube/callback"

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=agent_id # We pass agent_id as state
    )

    return RedirectResponse(authorization_url)


# =========================
# YOUTUBE OAUTH CALLBACK
# =========================
@router.get("/youtube/callback")
def youtube_callback(request: Request, state: str, code: str):
    """
    Handles the redirect from Google
    """
    agent_id = state

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

    base_url = str(request.base_url).rstrip('/')
    if not settings.DEBUG:
        base_url = base_url.replace("http://", "https://")
    flow.redirect_uri = f"{base_url}/agents/youtube/callback"

    flow.fetch_token(code=code)
    creds = flow.credentials

    # Update agent with tokens
    agent_service.update_agent(agent_id, {
        "youtube_access_token": creds.token,
        "youtube_refresh_token": creds.refresh_token,
        "youtube_token_expiry": creds.expiry
    })

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