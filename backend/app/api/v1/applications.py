from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from datetime import datetime

from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from app.models.profile import JobSeekerProfile, EmployerProfile
from app.core.security import get_current_user_id
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/")
async def apply_to_job(
    application_data: dict,
    user_id: str = Depends(get_current_user_id)
):
    """Apply to a job"""
    job_id = application_data.get("job_id")
    
    # Get job seeker profile
    profile = await JobSeekerProfile.find_one(JobSeekerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Job seeker profile not found")
    
    # Verify job exists
    job = await Job.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if already applied
    existing = await Application.find_one(
        Application.job_id == ObjectId(job_id),
        Application.job_seeker_id == profile.id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    # Create application
    application = Application(
        job_id=ObjectId(job_id),
        job_seeker_id=profile.id,
        cover_letter=application_data.get("cover_letter"),
        status=ApplicationStatus.SUBMITTED,
    )
    await application.insert()
    
    # Update job application count
    job.applications_count += 1
    await job.save()
    
    logger.info(f"Application created: job {job_id} by seeker {profile.id}")
    return application


@router.get("/")
async def get_my_applications(user_id: str = Depends(get_current_user_id)):
    """Get user's applications"""
    profile = await JobSeekerProfile.find_one(JobSeekerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    applications = await Application.find(
        Application.job_seeker_id == profile.id
    ).to_list()
    return applications


@router.get("/{application_id}")
async def get_application(
    application_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get application details"""
    application = await Application.get(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # TODO: Verify user has access to this application
    return application
