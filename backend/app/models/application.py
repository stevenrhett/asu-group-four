from beanie import Document
from pydantic import BaseModel
from typing import Literal


class Application(Document):
    job_id: str
    user_id: str
    status: Literal["applied", "viewed", "shortlisted", "interview", "rejected"] = "applied"

    class Settings:
        name = "applications"


class ApplicationCreate(BaseModel):
    job_id: str

