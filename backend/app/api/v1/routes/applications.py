"""
Application management endpoints (ST-014).

Handles job application submission and status tracking through
the application lifecycle.
"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from beanie import PydanticObjectId

from app.api.deps import get_current_user, require_role
from app.models.application import (
    Application,
    ApplicationCreate,
    ApplicationResponse,
    ApplicationWithHistory,
    ApplicationUpdate,
    ApplicationStatus,
    StatusChange
)
from app.models.job import Job
from app.models.user import User
from app.services.notifications import dispatch_status_notifications
from app.services.logging import logger as event_logger
from app.schemas.events import BaseEvent, EventType

router = APIRouter()


@router.post("/", response_model=ApplicationResponse, status_code=201)
async def apply_to_job(
    payload: ApplicationCreate,
    current_user: User = Depends(require_role("seeker"))
):
    """
    Submit an application to a job.
    
    Creates a new application record for the job. Idempotent - if the
    seeker has already applied to this job, returns the existing application.
    
    Requires seeker role.
    """
    # Verify job exists
    try:
        job = await Job.get(PydanticObjectId(payload.job_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if already applied (idempotency)
    existing = await Application.find_one(
        Application.job_id == payload.job_id,
        Application.user_id == str(current_user.id)
    )
    
    if existing:
        # Return existing application (idempotent)
        return ApplicationResponse.from_document(existing)
    
    # Create new application
    application = Application(
        job_id=payload.job_id,
        user_id=str(current_user.id),
        employer_id=job.employer_id,
        status=ApplicationStatus.APPLIED,
        cover_letter=payload.cover_letter,
        status_history=[
            StatusChange(
                from_status=None,
                to_status=ApplicationStatus.APPLIED,
                changed_by=str(current_user.id),
                changed_at=datetime.utcnow()
            )
        ]
    )
    await application.insert()
    
    # Log event
    event_logger.log_application_submitted(
        candidate_id=str(current_user.id),
        job_id=payload.job_id,
        application_id=str(application.id)
    )
    
    return ApplicationResponse.from_document(application)


@router.get("/", response_model=List[ApplicationResponse])
async def list_applications(
    status: Optional[ApplicationStatus] = Query(None, description="Filter by status"),
    job_id: Optional[str] = Query(None, description="Filter by job ID"),
    current_user: User = Depends(get_current_user)
):
    """
    List applications.
    
    - **Seekers** see only their own applications
    - **Employers** see all applications for their jobs
    - **Admin** sees all applications
    
    Supports filtering by status and job_id.
    """
    query_filters = []
    
    if current_user.role == "seeker":
        # Seekers only see their own applications
        query_filters.append(Application.user_id == str(current_user.id))
    elif current_user.role == "employer":
        # Employers see applications for their jobs
        query_filters.append(Application.employer_id == str(current_user.id))
    # Admin sees all (no filter needed)
    
    # Apply optional filters
    if status:
        query_filters.append(Application.status == status)
    if job_id:
        query_filters.append(Application.job_id == job_id)
    
    if query_filters:
        applications = await Application.find(*query_filters).to_list()
    else:
        applications = await Application.find_all().to_list()
    
    return [ApplicationResponse.from_document(app) for app in applications]


@router.get("/{application_id}", response_model=ApplicationWithHistory)
async def get_application(
    application_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific application with full history.
    
    Returns the application with complete status change history.
    Authorization: seekers can only view their own, employers can view
    applications for their jobs.
    """
    try:
        application = await Application.get(PydanticObjectId(application_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Authorization check
    if current_user.role == "seeker" and application.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    
    if current_user.role == "employer" and application.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    
    return ApplicationWithHistory.from_document(application)


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: str,
    payload: ApplicationUpdate,
    current_user: User = Depends(require_role("employer"))
):
    """
    Update application status.
    
    Employers can update the status of applications for their jobs.
    Records status changes in audit trail and sends notifications.
    
    Status flow: applied → viewed → shortlisted → interview (or rejected at any point)
    
    Requires employer role.
    """
    # Get application
    try:
        application = await Application.get(PydanticObjectId(application_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify employer owns this job
    if application.employer_id != str(current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this application"
        )
    
    # Check if status is actually changing (idempotency)
    if application.status == payload.status:
        # No change needed, return current state
        return ApplicationResponse.from_document(application)
    
    # Store old status for history
    old_status = application.status
    
    # Update status
    application.status = payload.status
    application.updated_at = datetime.utcnow()
    
    # Update specific timestamp based on new status
    if payload.status == ApplicationStatus.VIEWED:
        application.viewed_at = datetime.utcnow()
    elif payload.status == ApplicationStatus.SHORTLISTED:
        application.shortlisted_at = datetime.utcnow()
    elif payload.status == ApplicationStatus.INTERVIEW:
        application.interview_at = datetime.utcnow()
    elif payload.status == ApplicationStatus.REJECTED:
        application.rejected_at = datetime.utcnow()
    
    # Add to status history
    status_change = StatusChange(
        from_status=old_status,
        to_status=payload.status,
        changed_by=str(current_user.id),
        changed_at=datetime.utcnow(),
        notes=payload.notes
    )
    application.status_history.append(status_change)
    
    # Save application
    await application.save()
    
    # Log event
    event_logger.log_application_status_changed(
        candidate_id=application.user_id,
        job_id=application.job_id,
        application_id=str(application.id),
        previous_status=old_status.value,
        new_status=payload.status.value,
        actor_id=str(current_user.id)
    )
    
    # Send notification to seeker
    seeker = await User.get(PydanticObjectId(application.user_id))
    job = await Job.get(PydanticObjectId(application.job_id))
    
    if seeker and job:
        dispatch_status_notifications(
            application,
            seeker,
            current_user,
            job.title
        )
    
    return ApplicationResponse.from_document(application)


@router.get("/{application_id}/history", response_model=List[StatusChange])
async def get_application_history(
    application_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get status change history for an application.
    
    Returns complete audit trail of status changes.
    Authorization: seekers can only view their own, employers can view
    applications for their jobs.
    """
    try:
        application = await Application.get(PydanticObjectId(application_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Authorization check
    if current_user.role == "seeker" and application.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    
    if current_user.role == "employer" and application.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    
    return application.status_history


@router.delete("/{application_id}", status_code=204)
async def withdraw_application(
    application_id: str,
    current_user: User = Depends(require_role("seeker"))
):
    """
    Withdraw an application.
    
    Seekers can withdraw their own applications if not yet processed.
    Can only withdraw if status is still 'applied' or 'viewed'.
    
    Requires seeker role.
    """
    try:
        application = await Application.get(PydanticObjectId(application_id))
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify ownership
    if application.user_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to withdraw this application")
    
    # Check if withdrawal is allowed
    if application.status not in [ApplicationStatus.APPLIED, ApplicationStatus.VIEWED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot withdraw application with status '{application.status.value}'"
        )
    
    # Log event before deletion
    event_logger.log_event(
        BaseEvent(
            event_type=EventType.APPLICATION_WITHDRAWN,
            actor_id=str(current_user.id),
            metadata={
                "application_id": str(application.id),
                "job_id": application.job_id,
                "status": application.status.value
            }
        )
    )
    
    # Delete application
    await application.delete()
    
    return None
