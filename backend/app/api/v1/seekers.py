from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.profile import JobSeekerProfile
from app.models.user import User, UserRole
from app.core.security import get_current_user_id, require_role
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/me")
async def get_seeker_profile(user_id: str = Depends(require_role(UserRole.JOB_SEEKER.value))):
    """Get current job seeker profile"""
    profile = await JobSeekerProfile.find_one(JobSeekerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/me")
async def update_seeker_profile(
    profile_data: dict,
    user_id: str = Depends(require_role(UserRole.JOB_SEEKER.value))
):
    """Update job seeker profile"""
    profile = await JobSeekerProfile.find_one(JobSeekerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    for key, value in profile_data.items():
        if hasattr(profile, key):
            setattr(profile, key, value)
    
    profile.updated_at = datetime.utcnow()
    await profile.save()
    return profile


@router.post("/me/resume")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(require_role(UserRole.JOB_SEEKER.value))
):
    """Upload resume"""
    # TODO: Implement file upload and parsing
    return {"message": "Resume upload endpoint - to be implemented"}
