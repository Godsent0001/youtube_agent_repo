from fastapi import APIRouter, HTTPException
from app.db.session import db
from app.schemas.job import JobResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])

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
