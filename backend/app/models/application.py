from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field, BaseModel
from bson import ObjectId
from enum import Enum


class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    ACCEPTED = "accepted"


class StatusHistory(BaseModel):
    status: ApplicationStatus
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    changed_by: Optional[ObjectId] = None
    notes: Optional[str] = None


class Interview(BaseModel):
    scheduled_at: datetime
    location: Optional[str] = None
    interview_type: str  # "phone", "video", "in_person"
    notes: Optional[str] = None
    confirmed: bool = False


class ResumeSnapshot(BaseModel):
    file_name: str
    file_path: str


class Application(Document):
    job_id: ObjectId
    job_seeker_id: ObjectId
    
    # Application Data
    cover_letter: Optional[str] = None
    resume_snapshot: Optional[ResumeSnapshot] = None
    
    # AI Matching
    ai_match_score: Optional[float] = None  # 0-100
    match_explanation: Optional[str] = None
    
    # Status
    status: ApplicationStatus = ApplicationStatus.SUBMITTED
    status_history: List[StatusHistory] = []
    
    # Interview
    interview: Optional[Interview] = None
    
    # Metadata
    viewed_by_employer: bool = False
    viewed_at: Optional[datetime] = None
    
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "applications"
        indexes = [
            "job_id",
            "job_seeker_id",
            "status",
            "ai_match_score",
            "applied_at",
            [("job_id", 1), ("job_seeker_id", 1)],  # Compound unique index
        ]


class Notification(Document):
    user_id: ObjectId
    
    # Notification Details
    type: str  # "application_status", "new_job_match", "interview_scheduled"
    title: str
    message: str
    
    # Related Entity
    related_entity_type: Optional[str] = None  # "job", "application"
    related_entity_id: Optional[ObjectId] = None
    
    # Status
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    # Delivery
    sent_via_email: bool = False
    email_sent_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notifications"
        indexes = [
            "user_id",
            "is_read",
            "created_at",
            [("user_id", 1), ("is_read", 1), ("created_at", -1)],
        ]
