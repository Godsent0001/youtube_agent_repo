from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List

from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services.agent_service import agent_service
from app.workers.worker import worker

router = APIRouter(prefix="/agents", tags=["Agents"])


# =========================
# CREATE AGENT
# =========================
@router.post("/", response_model=str)
def create_agent(payload: AgentCreate, user_id: str):

    agent_id = agent_service.create_agent(
        user_id=user_id,
        data=payload.dict()
    )

    return agent_id


# =========================
# GET ALL USER AGENTS
# =========================
@router.get("/", response_model=List[dict])
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
    pushes job into worker queue
    """

    worker.add_job("generate_video", {
        "agent_id": agent_id
    })

    return {
        "message": "Video generation started",
        "agent_id": agent_id
    }