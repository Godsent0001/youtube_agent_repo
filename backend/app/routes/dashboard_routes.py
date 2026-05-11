from fastapi import APIRouter
from typing import List

from app.services.analytics.metrics_service import metrics_service
from app.services.agent_service import agent_service
from app.services.video.video_service import video_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================
# OVERALL USER DASHBOARD
# =========================
@router.get("/overview")
def get_overview(user_id: str):

    agents = agent_service.list_user_agents(user_id)
    videos = video_service.get_user_videos(user_id)

    metrics = metrics_service.get_user_summary(user_id)

    return {
        "total_agents": len(agents),
        "total_videos": len(videos),
        "total_views": metrics.get("views", 0),
        "avg_retention": metrics.get("retention_rate", 0),
        "avg_ctr": metrics.get("ctr", 0)
    }


# =========================
# AGENT PERFORMANCE
# =========================
@router.get("/agents/{agent_id}")
def agent_performance(agent_id: str):

    agent_metrics = metrics_service.get_agent_metrics(agent_id)

    return {
        "agent_id": agent_id,
        "metrics": agent_metrics
    }


# =========================
# VIDEO PERFORMANCE LIST
# =========================
@router.get("/videos")
def get_videos(user_id: str):

    videos = video_service.get_user_videos(user_id)

    return videos


# =========================
# SINGLE VIDEO ANALYTICS
# =========================
@router.get("/videos/{video_id}")
def video_details(video_id: str):

    video = video_service.get_video(video_id)
    metrics = metrics_service.get_video_metrics(video_id)

    return {
        "video": video,
        "metrics": metrics
    }


# =========================
# LEARNING INSIGHTS (AI INPUT)
# =========================
@router.get("/insights")
def learning_insights(user_id: str):

    insights = metrics_service.generate_learning_insights(user_id)

    return {
        "insights": insights
    }