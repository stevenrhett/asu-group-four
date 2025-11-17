from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field, BaseModel
from bson import ObjectId
from enum import Enum


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class JobStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"


class JobLocation(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "USA"
    is_remote: bool = False
    remote_type: Optional[str] = None  # "remote", "hybrid", "on_site"


class Job(Document):
    employer_id: ObjectId
    
    # Job Details
    title: str
    description: str
    requirements: List[str] = []
    responsibilities: List[str] = []
    
    # Job Specs
    job_type: JobType
    experience_level: ExperienceLevel
    skills_required: List[str] = []
    education_required: Optional[str] = None
    
    # Compensation
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    
    # Location
    location: JobLocation
    
    # Employment Details
    industry: Optional[str] = None
    department: Optional[str] = None
    
    # Application Settings
    application_deadline: Optional[datetime] = None
    spots_available: Optional[int] = None
    
    # Status
    status: JobStatus = JobStatus.ACTIVE
    
    # AI Embeddings
    job_embedding: Optional[List[float]] = None
    
    # Metadata
    views_count: int = 0
    applications_count: int = 0
    
    posted_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "jobs"
        indexes = [
            "employer_id",
            "status",
            "job_type",
            "experience_level",
            "skills_required",
            "location.city",
            "posted_at",
        ]
