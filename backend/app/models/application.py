"""
Application model for job applications and status tracking (ST-014).

Tracks the lifecycle of job applications from submission through
various status changes (viewed, shortlisted, interview, rejected).
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from beanie import Document
from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    APPLIED = "applied"
    VIEWED = "viewed"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    REJECTED = "rejected"


class StatusChange(BaseModel):
    """Record of a status change for audit trail."""
    from_status: Optional[ApplicationStatus] = None
    to_status: ApplicationStatus
    changed_by: str  # User ID who made the change
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None


class Application(Document):
    """
    Job application with status tracking and audit trail.
    
    Tracks the complete lifecycle of an application from submission
    through various employer actions.
    """
    job_id: str
    user_id: str  # Seeker who applied
    employer_id: Optional[str] = None  # Employer who owns the job
    status: ApplicationStatus = ApplicationStatus.APPLIED
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    viewed_at: Optional[datetime] = None
    shortlisted_at: Optional[datetime] = None
    interview_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    
    # Audit trail
    status_history: List[StatusChange] = Field(default_factory=list)
    
    # Application details
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None

    class Settings:
        name = "applications"


class ApplicationCreate(BaseModel):
    """Schema for creating a new job application."""
    job_id: str
    cover_letter: Optional[str] = Field(None, max_length=2000)


class ApplicationUpdate(BaseModel):
    """Schema for updating application status."""
    status: ApplicationStatus
    notes: Optional[str] = Field(None, max_length=500)


class ApplicationResponse(BaseModel):
    """Schema for application response."""
    id: str
    job_id: str
    user_id: str
    employer_id: Optional[str]
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    viewed_at: Optional[datetime]
    shortlisted_at: Optional[datetime]
    interview_at: Optional[datetime]
    rejected_at: Optional[datetime]
    cover_letter: Optional[str]
    
    @classmethod
    def from_document(cls, doc: Application) -> "ApplicationResponse":
        return cls(
            id=str(doc.id),
            job_id=doc.job_id,
            user_id=doc.user_id,
            employer_id=doc.employer_id,
            status=doc.status,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            viewed_at=doc.viewed_at,
            shortlisted_at=doc.shortlisted_at,
            interview_at=doc.interview_at,
            rejected_at=doc.rejected_at,
            cover_letter=doc.cover_letter
        )


class ApplicationWithHistory(ApplicationResponse):
    """Application response with full status history."""
    status_history: List[StatusChange]
    
    @classmethod
    def from_document(cls, doc: Application) -> "ApplicationWithHistory":
        base = ApplicationResponse.from_document(doc)
        return cls(
            **base.model_dump(),
            status_history=doc.status_history
        )


# Legacy alias for backwards compatibility
ApplicationPublic = ApplicationResponse
