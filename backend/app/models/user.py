from datetime import datetime
from typing import Literal, Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class User(Document):
    email: EmailStr
    hashed_password: str
    role: Literal["seeker", "employer"]
    
    # Contact information
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None
    
    # Account status
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    class Settings:
        name = "users"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["seeker", "employer"]


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: Literal["seeker", "employer"]
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None


class UserDeleteRequest(BaseModel):
    password: str

