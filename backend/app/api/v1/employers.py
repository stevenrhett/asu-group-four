from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from datetime import datetime

from app.models.profile import EmployerProfile
from app.models.user import UserRole
from app.core.security import require_role
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/me")
async def get_employer_profile(user_id: str = Depends(require_role(UserRole.EMPLOYER.value))):
    """Get current employer profile"""
    profile = await EmployerProfile.find_one(EmployerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/me")
async def update_employer_profile(
    profile_data: dict,
    user_id: str = Depends(require_role(UserRole.EMPLOYER.value))
):
    """Update employer profile"""
    profile = await EmployerProfile.find_one(EmployerProfile.user_id == ObjectId(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in profile_data.items():
        if hasattr(profile, key):
            setattr(profile, key, value)
    
    profile.updated_at = datetime.utcnow()
    await profile.save()
    return profile
