from fastapi import APIRouter, HTTPException
from app.db.session import db
from app.schemas.job import JobResponse
from typing import List

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/agent/{agent_id}", response_model=List[JobResponse])
def get_agent_jobs(agent_id: str):
    """
    Fetch all background jobs for a specific agent
    """
    jobs = list(db["jobs"].find({"agent_id": agent_id}).sort("created_at", -1).limit(20))

    for job in jobs:
        job["id"] = str(job["_id"])

    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str):
    """
    Fetch the current status of a background job from MongoDB
    """
    job = db["jobs"].find_one({"job_id": job_id})

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # MongoDB _id to string for pydantic
    job["id"] = str(job["_id"])

    return job
