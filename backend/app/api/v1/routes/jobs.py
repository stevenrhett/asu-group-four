"""
Job posting management endpoints.

Allows employers to create, edit, archive, and manage job postings.
"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from beanie import PydanticObjectId

from app.models.job import Job, JobCreate, JobUpdate, JobResponse, JobStatus
from app.api.deps import require_role, get_current_user
from app.models.user import User
from app.services.logging import logger as event_logger
from app.schemas.events import BaseEvent, EventType, EventSeverity

router = APIRouter()


def job_to_response(job: Job) -> JobResponse:
    """Convert Job document to JobResponse schema."""
    return JobResponse(
        id=str(job.id),
        title=job.title,
        description=job.description,
        skills=job.skills,
        employer_id=job.employer_id,
        status=job.status,
        location=job.location,
        city=job.city,
        state=job.state,
        country=job.country,
        work_type=job.work_type,
        job_type=job.job_type,
        experience_level=job.experience_level,
        easy_apply=job.easy_apply,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        company_name=job.company_name,
        company_rating=job.company_rating,
        company_size=job.company_size,
        industry=job.industry,
        posted_at=job.posted_at,
        created_at=job.created_at,
        updated_at=job.updated_at,
        archived_at=job.archived_at
    )


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[JobStatus] = Query(None, description="Filter by job status"),
    employer_id: Optional[str] = Query(None, description="Filter by employer ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    List all jobs with optional filtering.
    
    - **status**: Filter by job status (active, archived, draft)
    - **employer_id**: Filter by employer ID
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    query = {}
    
    if status:
        query["status"] = status
    if employer_id:
        query["employer_id"] = employer_id
    
    jobs = await Job.find(query).skip(skip).limit(limit).to_list()
    
    return [job_to_response(job) for job in jobs]


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get a specific job by ID."""
    job = await Job.get(PydanticObjectId(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_to_response(job)


@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    payload: JobCreate,
    current_user: User = Depends(require_role("employer"))
):
    """
    Create a new job posting.
    
    Requires employer role.
    """
    job = Job(
        **payload.model_dump(),
        employer_id=str(current_user.id),
        status=JobStatus.ACTIVE,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await job.insert()
    
    # Log the event
    event_logger.log_event(
        BaseEvent(
            event_type=EventType.JOB_POSTED,
            actor_id=str(current_user.id),
            metadata={
                "job_id": str(job.id),
                "title": job.title,
                "skills": job.skills
            }
        )
    )
    
    return job_to_response(job)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    payload: JobUpdate,
    current_user: User = Depends(require_role("employer"))
):
    """
    Update an existing job posting.
    
    Requires employer role. Only the job owner can update.
    """
    job = await Job.get(PydanticObjectId(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify ownership
    if job.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this job")
    
    # Update only provided fields
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(job, field, value)
        job.updated_at = datetime.utcnow()
        await job.save()
        
        # Log the event
        event_logger.log_event(
            BaseEvent(
                event_type=EventType.JOB_UPDATED,
                actor_id=str(current_user.id),
                metadata={
                    "job_id": str(job.id),
                    "updated_fields": list(update_data.keys())
                }
            )
        )
    
    return job_to_response(job)


@router.patch("/{job_id}/archive", response_model=JobResponse)
async def archive_job(
    job_id: str,
    current_user: User = Depends(require_role("employer"))
):
    """
    Archive a job posting.
    
    Archived jobs no longer appear in active listings.
    Requires employer role. Only the job owner can archive.
    """
    job = await Job.get(PydanticObjectId(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify ownership
    if job.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to archive this job")
    
    if job.status == JobStatus.ARCHIVED:
        raise HTTPException(status_code=400, detail="Job is already archived")
    
    job.status = JobStatus.ARCHIVED
    job.archived_at = datetime.utcnow()
    job.updated_at = datetime.utcnow()
    await job.save()
    
    # Log the event
    event_logger.log_event(
        BaseEvent(
            event_type=EventType.JOB_ARCHIVED,
            actor_id=str(current_user.id),
            metadata={
                "job_id": str(job.id),
                "title": job.title
            }
        )
    )
    
    return job_to_response(job)


@router.patch("/{job_id}/unarchive", response_model=JobResponse)
async def unarchive_job(
    job_id: str,
    current_user: User = Depends(require_role("employer"))
):
    """
    Unarchive a job posting.
    
    Reactivates an archived job.
    Requires employer role. Only the job owner can unarchive.
    """
    job = await Job.get(PydanticObjectId(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify ownership
    if job.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to unarchive this job")
    
    if job.status != JobStatus.ARCHIVED:
        raise HTTPException(status_code=400, detail="Job is not archived")
    
    job.status = JobStatus.ACTIVE
    job.archived_at = None
    job.updated_at = datetime.utcnow()
    await job.save()
    
    # Log the event
    event_logger.log_event(
        BaseEvent(
            event_type=EventType.JOB_UNARCHIVED,
            actor_id=str(current_user.id),
            metadata={
                "job_id": str(job.id),
                "title": job.title
            }
        )
    )
    
    return job_to_response(job)


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: str,
    current_user: User = Depends(require_role("employer"))
):
    """
    Permanently delete a job posting.
    
    Requires employer role. Only the job owner can delete.
    Use archive instead for soft deletion.
    """
    job = await Job.get(PydanticObjectId(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify ownership
    if job.employer_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    
    # Log the event before deletion
    event_logger.log_event(
        BaseEvent(
            event_type=EventType.JOB_DELETED,
            actor_id=str(current_user.id),
            metadata={
                "job_id": str(job.id),
                "title": job.title
            }
        )
    )
    
    await job.delete()
    return None
