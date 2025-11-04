from beanie import Document
from pydantic import BaseModel
from typing import List, Optional


class Job(Document):
    title: str
    description: str
    location: Optional[str] = None
    skills: List[str] = []

    class Settings:
        name = "jobs"


class JobCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    skills: List[str] = []

