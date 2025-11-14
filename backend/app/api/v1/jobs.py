from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.job import Job, JobStatus
from app.models.profile import EmployerProfile
from app.models.user import UserRole
from app.core.security import get_current_user_id, require_role
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/")
async def search_jobs(
    q: Optional[str] = None,
    job_type: Optional[str] = None,
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    """Search jobs"""
    query = {"status": JobStatus.ACTIVE}
    
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]
    
    if job_type:
        query["job_type"] = job_type
    
    if location:
        query["location.city"] = {"$regex": location, "$options": "i"}
    
    jobs = await Job.find(query).skip(skip).limit(limit).to_list()
    return jobs


@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get job details"""
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Increment view count
    job.views_count += 1
    await job.save()
    
    return job


@router.post("/")
async def create_job(
    job_data: dict,
    user_id: str = Depends(require_role(UserRole.EMPLOYER.value))
):
    """Create job posting"""
    # Get employer profile
    profile = await EmployerProfile.find_one(EmployerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Employer profile not found")
    
    # Create job - basic implementation
    job = Job(
        employer_id=profile.id,
        **job_data
    )
    await job.insert()
    
    logger.info(f"Job created: {job.title} by employer {profile.company_name}")
    return job


@router.put("/{job_id}")
async def update_job(
    job_id: str,
    job_data: dict,
    user_id: str = Depends(require_role(UserRole.EMPLOYER.value))
):
    """Update job posting"""
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify ownership
    profile = await EmployerProfile.find_one(EmployerProfile.user_id == ObjectId(user_id))
    if not profile or job.employer_id != profile.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in job_data.items():
        if hasattr(job, key):
            setattr(job, key, value)
    
    job.updated_at = datetime.utcnow()
    await job.save()
    return job


@router.get("/my-jobs")
async def get_my_jobs(user_id: str = Depends(require_role(UserRole.EMPLOYER.value))):
    """Get employer's job postings"""
    profile = await EmployerProfile.find_one(EmployerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    jobs = await Job.find(Job.employer_id == profile.id).to_list()
    return jobs
