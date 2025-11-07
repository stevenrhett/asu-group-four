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


class Job(Document):
    title: str
    description: str
    location: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    employer_id: Optional[str] = None  # ID of the employer who posted the job
    status: JobStatus = JobStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    archived_at: Optional[datetime] = None
    
    # Indexing fields
    tokens: List[str] = Field(default_factory=list)
    normalized_text: Optional[str] = None
    embedding: Optional[List[float]] = None
    indexed_at: Optional[datetime] = None

    class Settings:
        name = "jobs"


class JobCreate(BaseModel):
    """Schema for creating a new job posting."""
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=5000)
    location: Optional[str] = Field(None, max_length=200)
    skills: List[str] = Field(default_factory=list)


class JobUpdate(BaseModel):
    """Schema for updating an existing job posting."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    location: Optional[str] = Field(None, max_length=200)
    skills: Optional[List[str]] = None


class JobResponse(BaseModel):
    """Schema for job response."""
    id: str
    title: str
    description: str
    location: Optional[str]
    skills: List[str]
    employer_id: Optional[str]
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime] = None
