from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel


class Profile(Document):
    user_id: str
    skills: List[str] = []
    titles: List[str] = []
    raw_text: Optional[str] = None
    resume_path: Optional[str] = None
    parsed_at: datetime = datetime.utcnow()

    class Settings:
        name = "profiles"
        indexes = ["user_id"]


class ProfilePublic(BaseModel):
    id: str
    user_id: str
    skills: List[str]
    titles: List[str]
    raw_text: Optional[str]
    parsed_at: Optional[datetime]

    @classmethod
    def from_document(cls, profile: Profile) -> "ProfilePublic":
        return cls(
            id=str(profile.id),
            user_id=profile.user_id,
            skills=profile.skills,
            titles=profile.titles,
            raw_text=profile.raw_text,
            parsed_at=profile.parsed_at,
        )
