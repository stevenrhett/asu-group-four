from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.job import JobType, ExperienceLevel, JobLocation


class JobCreateSchema(BaseModel):
    """Schema for creating a new job"""
    title: str = Field(..., min_length=3, max_length=200, description="Job title")
    description: str = Field(..., min_length=50, max_length=10000, description="Job description")
    requirements: List[str] = Field(default_factory=list, max_items=50)
    responsibilities: List[str] = Field(default_factory=list, max_items=50)

    job_type: JobType
    experience_level: ExperienceLevel
    skills_required: List[str] = Field(default_factory=list, max_items=50)
    education_required: Optional[str] = Field(None, max_length=500)

    salary_min: Optional[int] = Field(None, ge=0, le=10000000)
    salary_max: Optional[int] = Field(None, ge=0, le=10000000)
    salary_currency: str = Field(default="USD", max_length=3)

    location: JobLocation

    industry: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)

    application_deadline: Optional[datetime] = None
    spots_available: Optional[int] = Field(None, ge=1, le=1000)

    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        """Ensure salary_max >= salary_min"""
        if v is not None and 'salary_min' in values and values['salary_min'] is not None:
            if v < values['salary_min']:
                raise ValueError('Maximum salary must be greater than or equal to minimum salary')
        return v

    @validator('title', 'description')
    def validate_no_xss(cls, v):
        """Basic XSS protection"""
        if v and any(char in v for char in ['<script>', '</script>', '<iframe>', 'javascript:']):
            raise ValueError('Invalid characters detected')
        return v

    class Config:
        use_enum_values = True


class JobUpdateSchema(BaseModel):
    """Schema for updating an existing job"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=50, max_length=10000)
    requirements: Optional[List[str]] = Field(None, max_items=50)
    responsibilities: Optional[List[str]] = Field(None, max_items=50)

    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    skills_required: Optional[List[str]] = Field(None, max_items=50)
    education_required: Optional[str] = Field(None, max_length=500)

    salary_min: Optional[int] = Field(None, ge=0, le=10000000)
    salary_max: Optional[int] = Field(None, ge=0, le=10000000)

    location: Optional[JobLocation] = None

    industry: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)

    application_deadline: Optional[datetime] = None
    spots_available: Optional[int] = Field(None, ge=1, le=1000)

    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        """Ensure salary_max >= salary_min if both provided"""
        if v is not None and 'salary_min' in values and values['salary_min'] is not None:
            if v < values['salary_min']:
                raise ValueError('Maximum salary must be greater than or equal to minimum salary')
        return v

    class Config:
        use_enum_values = True
