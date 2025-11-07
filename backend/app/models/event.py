from datetime import datetime
from typing import Any, Dict, Optional

from beanie import Document
from pydantic import BaseModel, Field


class EventLog(Document):
    event_type: str
    actor_id: Optional[str] = None
    subject_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "events"


class EventCreate(BaseModel):
    event_type: str
    actor_id: Optional[str] = None
    subject_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
