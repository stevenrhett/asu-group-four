from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User, UserPublic, UserUpdate, UserDeleteRequest
from app.models.profile import Profile
from app.models.application import Application
from app.models.event import EventLog, EventCreate

router = APIRouter()


@router.get("/me", response_model=UserPublic)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile with contact information and account details."""
    return UserPublic(
        id=str(current_user.id),
        email=current_user.email,
        role=current_user.role,
        phone=current_user.phone,
        linkedin_url=current_user.linkedin_url,
        website_url=current_user.website_url,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.patch("/me", response_model=UserPublic)
async def update_user_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update user's contact information."""
    # Update only provided fields
    if payload.phone is not None:
        current_user.phone = payload.phone
    if payload.linkedin_url is not None:
        current_user.linkedin_url = payload.linkedin_url
    if payload.website_url is not None:
        current_user.website_url = payload.website_url
    
    await current_user.save()
    
    return UserPublic(
        id=str(current_user.id),
        email=current_user.email,
        role=current_user.role,
        phone=current_user.phone,
        linkedin_url=current_user.linkedin_url,
        website_url=current_user.website_url,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.post("/me/deactivate")
async def deactivate_account(current_user: User = Depends(get_current_user)):
    """Soft delete: deactivate user account (can be reactivated by support)."""
    current_user.is_active = False
    await current_user.save()
    
    # Log deactivation event for audit
    event = EventLog(
        event_type="account_deactivated",
        user_id=str(current_user.id),
        metadata={"email": current_user.email, "role": current_user.role},
        timestamp=datetime.utcnow()
    )
    await event.insert()
    
    return {"message": "Account deactivated successfully"}


@router.delete("/me")
async def delete_account_permanently(
    payload: UserDeleteRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Permanently delete user account (GDPR compliance).
    
    This operation:
    1. Verifies password for security
    2. Anonymizes all applications
    3. Deletes profile and resume files
    4. Logs deletion for audit trail
    5. Permanently removes user record
    """
    # Verify password for security
    if not verify_password(payload.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    user_id = str(current_user.id)
    user_email = current_user.email
    
    # 1. Anonymize all applications (GDPR compliance)
    applications = await Application.find(Application.user_id == user_id).to_list()
    for app in applications:
        app.user_id = "deleted_user"
        await app.save()
    
    # 2. Delete profile and resume files
    profile = await Profile.find_one(Profile.user_id == user_id)
    if profile:
        # Delete resume file from storage
        if profile.resume_path:
            resume_file = Path(profile.resume_path)
            if resume_file.exists():
                resume_file.unlink()
        
        # Delete profile document
        await profile.delete()
    
    # 3. Log deletion event for compliance audit trail
    event = EventLog(
        event_type="account_deleted_permanently",
        user_id=user_id,
        metadata={
            "email": user_email,
            "role": current_user.role,
            "applications_anonymized": len(applications),
            "profile_deleted": profile is not None
        },
        timestamp=datetime.utcnow()
    )
    await event.insert()
    
    # 4. Mark user as deleted with timestamp
    current_user.deleted_at = datetime.utcnow()
    current_user.is_active = False
    await current_user.save()
    
    # 5. Permanently delete user record
    await current_user.delete()
    
    return {"message": "Account permanently deleted"}

