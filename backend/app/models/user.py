from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"


class User(Document):
    email: EmailStr = Field(..., unique=True)
    password_hash: str
    role: UserRole
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "role",
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "role": "job_seeker",
                "is_active": True,
            }
        }
