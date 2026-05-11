from fastapi import APIRouter, HTTPException

from app.services.agent_service import agent_service

router = APIRouter(prefix="/settings", tags=["Settings"])


# =========================
# GET AGENT SETTINGS
# =========================
@router.get("/agent/{agent_id}")
def get_agent_settings(agent_id: str):

    agent = agent_service.get_agent(agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "agent_id": agent_id,
        "name": agent.get("name"),
        "niche": agent.get("niche"),
        "content_type": agent.get("content_type"),
        "custom_prompt": agent.get("custom_prompt"),
        "posting_frequency": agent.get("posting_frequency")
    }


# =========================
# UPDATE AGENT SETTINGS
# =========================
@router.put("/agent/{agent_id}")
def update_agent_settings(agent_id: str, payload: dict):

    updated = agent_service.update_agent(
        agent_id,
        payload
    )

    return {
        "message": "Settings updated successfully",
        "agent": updated
    }


# =========================
# RESET TO DEFAULT AI SETTINGS
# =========================
@router.post("/agent/{agent_id}/reset")
def reset_agent_settings(agent_id: str):

    default_settings = {
        "custom_prompt": None,
        "posting_frequency": "daily"
    }

    updated = agent_service.update_agent(agent_id, default_settings)

    return {
        "message": "Agent reset to AI default settings",
        "agent": updated
    }