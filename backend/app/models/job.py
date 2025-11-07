from datetime import datetime
from typing import List, Optional
from enum import Enum

from beanie import Document
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job status enumeration."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


class WorkType(str, Enum):
    """Work type enumeration for remote/hybrid/onsite."""
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class JobType(str, Enum):
    """Job type enumeration for employment type."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class ExperienceLevel(str, Enum):
    """Experience level enumeration."""
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"


class CompanySize(str, Enum):
    """Company size enumeration."""
    STARTUP = "startup"  # 1-50 employees
    SMALL = "small"      # 51-200 employees
    MEDIUM = "medium"    # 201-1000 employees
    LARGE = "large"      # 1001-10000 employees
    ENTERPRISE = "enterprise"  # 10000+ employees


class Job(Document):
    # Core fields
    title: str
    description: str
    skills: List[str] = Field(default_factory=list)
    employer_id: Optional[str] = None  # ID of the employer who posted the job
    status: JobStatus = JobStatus.ACTIVE
    
    # Filter fields - Location
    location: Optional[str] = None  # Full location string
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "USA"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Filter fields - Work arrangement
    work_type: WorkType = WorkType.ONSITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.MID
    easy_apply: bool = False
    
    # Filter fields - Salary
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    
    # Filter fields - Company
    company_name: Optional[str] = None
    company_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    company_size: Optional[CompanySize] = None
    industry: Optional[str] = None
    
    # Timestamps
    posted_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    archived_at: Optional[datetime] = None
    
    # Indexing fields (for AI recommendations)
    tokens: List[str] = Field(default_factory=list)
    normalized_text: Optional[str] = None
    embedding: Optional[List[float]] = None
    indexed_at: Optional[datetime] = None

    class Settings:
        name = "jobs"
        indexes = [
            "posted_at",
            "work_type",
            "job_type",
            "experience_level",
            "salary_min",
            "salary_max",
            "company_rating",
            "city",
            "status",
        ]


class JobCreate(BaseModel):
    """Schema for creating a new job posting."""
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    skills: List[str] = Field(default_factory=list)
    
    # Location fields
    location: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)
    country: str = "USA"
    
    # Work arrangement
    work_type: WorkType = WorkType.ONSITE
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.MID
    easy_apply: bool = False
    
    # Salary
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: str = "USD"
    
    # Company
    company_name: Optional[str] = Field(None, max_length=200)
    company_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    company_size: Optional[CompanySize] = None
    industry: Optional[str] = Field(None, max_length=100)


class JobUpdate(BaseModel):
    """Schema for updating an existing job posting."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    skills: Optional[List[str]] = None
    
    # Location fields
    location: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = None
    
    # Work arrangement
    work_type: Optional[WorkType] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    easy_apply: Optional[bool] = None
    
    # Salary
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    
    # Company
    company_name: Optional[str] = Field(None, max_length=200)
    company_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    company_size: Optional[CompanySize] = None
    industry: Optional[str] = Field(None, max_length=100)


class JobResponse(BaseModel):
    """Schema for job response."""
    id: str
    title: str
    description: str
    skills: List[str]
    employer_id: Optional[str]
    status: JobStatus
    
    # Location fields
    location: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: str
    
    # Work arrangement
    work_type: WorkType
    job_type: JobType
    experience_level: ExperienceLevel
    easy_apply: bool
    
    # Salary
    salary_min: Optional[int]
    salary_max: Optional[int]
    salary_currency: str
    
    # Company
    company_name: Optional[str]
    company_rating: Optional[float]
    company_size: Optional[CompanySize]
    industry: Optional[str]
    
    # Timestamps
    posted_at: datetime
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime] = None
