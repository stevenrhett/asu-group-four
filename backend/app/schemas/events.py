"""
Event schemas for structured logging and observability.

Defines standardized event types for tracking user actions,
system events, and errors across the application.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class EventType(str, Enum):
    """Enumeration of all event types in the system."""
    
    # Recommendation events
    RECOMMENDATION_VIEW = "recommendation.view"
    RECOMMENDATION_CLICK = "recommendation.click"
    
    # Application events
    APPLICATION_SUBMITTED = "application.submitted"
    APPLICATION_STATUS_CHANGED = "application.status_changed"
    APPLICATION_WITHDRAWN = "application.withdrawn"
    
    # Inbox events
    INBOX_CANDIDATE_VIEWED = "inbox.candidate_viewed"
    INBOX_CANDIDATE_SHORTLISTED = "inbox.candidate_shortlisted"
    INBOX_CANDIDATE_REJECTED = "inbox.candidate_rejected"
    
    # Feedback events
    FEEDBACK_SUBMITTED = "feedback.submitted"
    
    # Resume events
    RESUME_UPLOADED = "resume.uploaded"
    RESUME_PARSED = "resume.parsed"
    
    # Job events
    JOB_POSTED = "job.posted"
    JOB_INDEXED = "job.indexed"
    JOB_UPDATED = "job.updated"
    JOB_ARCHIVED = "job.archived"
    JOB_UNARCHIVED = "job.unarchived"
    JOB_DELETED = "job.deleted"
    
    # Error events
    ERROR_OCCURRED = "error.occurred"
    
    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    
    # SLA/Performance events
    SLA_LATENCY_BUDGET_EXCEEDED = "sla.latency_budget_exceeded"
    SLA_ERROR_BUDGET_EXCEEDED = "sla.error_budget_exceeded"


class EventSeverity(str, Enum):
    """Event severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class BaseEvent(BaseModel):
    """Base event schema with common fields."""
    
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None
    actor_id: Optional[str] = None  # User ID (anonymized if needed)
    severity: EventSeverity = EventSeverity.INFO
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RecommendationEvent(BaseEvent):
    """Event for recommendation-related actions."""
    
    job_id: str
    candidate_id: str
    score: Optional[float] = None
    rank: Optional[int] = None
    context: Optional[str] = None  # e.g., "homepage", "search_results"


class ApplicationEvent(BaseEvent):
    """Event for job application actions."""
    
    application_id: str
    job_id: str
    candidate_id: str
    previous_status: Optional[str] = None
    new_status: Optional[str] = None


class InboxEvent(BaseEvent):
    """Event for employer inbox actions."""
    
    employer_id: str
    candidate_id: str
    job_id: str
    action: str  # viewed, shortlisted, rejected, etc.
    time_since_application: Optional[float] = None  # seconds


class FeedbackEvent(BaseEvent):
    """Event for user feedback."""
    
    user_id: str
    feedback_type: str  # thumbs_up, thumbs_down, comment
    target_type: str  # recommendation, job, system
    target_id: str
    feedback_text: Optional[str] = None


class ResumeEvent(BaseEvent):
    """Event for resume upload and processing."""
    
    candidate_id: str
    resume_id: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    parsing_duration: Optional[float] = None  # seconds
    success: bool = True


class JobEvent(BaseEvent):
    """Event for job posting and indexing."""
    
    job_id: str
    employer_id: str
    job_title: Optional[str] = None
    indexing_duration: Optional[float] = None  # seconds
    success: bool = True


class ErrorEvent(BaseEvent):
    """Event for errors and exceptions."""
    
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    request_path: Optional[str] = None
    request_method: Optional[str] = None
    user_id: Optional[str] = None
    
    def __init__(self, **data):
        if "severity" not in data:
            data["severity"] = EventSeverity.ERROR
        if "event_type" not in data:
            data["event_type"] = EventType.ERROR_OCCURRED
        super().__init__(**data)


class SystemEvent(BaseEvent):
    """Event for system-level actions."""
    
    service_name: str
    environment: Optional[str] = None
    version: Optional[str] = None
