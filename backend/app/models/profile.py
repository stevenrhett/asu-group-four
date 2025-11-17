from datetime import datetime
from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from enum import Enum
from app.models.user import User


class RemoteType(str, Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on_site"
    ANY = "any"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class Location(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "USA"
    zip_code: Optional[str] = None


class Experience(BaseModel):
    company: str
    title: str
    location: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    skills_used: List[str] = []


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None


class Resume(BaseModel):
    file_name: str
    file_path: str
    file_size: int
    content_type: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    parsed_text: Optional[str] = None


class JobPreferences(BaseModel):
    job_types: List[JobType] = []
    desired_salary_min: Optional[int] = None
    desired_salary_max: Optional[int] = None
    willing_to_relocate: bool = False
    preferred_locations: List[str] = []
    remote_preference: RemoteType = RemoteType.ANY
    industries: List[str] = []


class JobSeekerProfile(Document):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    user_id: ObjectId = Field(..., unique=True)
    
    # Personal Info
    first_name: str
    last_name: str
    phone: Optional[str] = None
    location: Optional[Location] = None
    
    # Professional Info
    headline: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []
    
    # Resume
    resume: Optional[Resume] = None
    
    # Preferences
    preferences: JobPreferences = Field(default_factory=JobPreferences)
    
    # AI Embeddings
    profile_embedding: Optional[List[float]] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "job_seeker_profiles"
        indexes = [
            "user_id",
            "skills",
            "location.city",
        ]


class EmployerProfile(Document):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    user_id: ObjectId = Field(..., unique=True)
    
    # Company Info
    company_name: str
    company_website: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    
    # Contact
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[Location] = None
    logo_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "employer_profiles"
        indexes = [
            "user_id",
            "company_name",
            "industry",
        ]
