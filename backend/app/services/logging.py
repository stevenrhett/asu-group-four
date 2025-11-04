"""
Structured logging service for event tracking and observability.

Provides centralized logging with correlation IDs, structured events,
and integration with monitoring systems.
"""
import json
import logging
import sys
import uuid
from contextvars import ContextVar
from datetime import datetime
from typing import Any, Dict, Optional

from app.schemas.events import (
    BaseEvent,
    EventType,
    EventSeverity,
    RecommendationEvent,
    ApplicationEvent,
    InboxEvent,
    FeedbackEvent,
    ResumeEvent,
    JobEvent,
    ErrorEvent,
    SystemEvent,
)

# Context variable for correlation ID (request tracking)
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class StructuredLogger:
    """
    Structured logger with JSON output for easy parsing and indexing.
    """
    
    def __init__(self, name: str = "job_portal"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure structured JSON logging."""
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(JsonFormatter())
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _add_correlation_id(self, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Add correlation ID to event if available."""
        correlation_id = correlation_id_var.get()
        if correlation_id and "correlation_id" not in event_dict:
            event_dict["correlation_id"] = correlation_id
        return event_dict
    
    def log_event(self, event: BaseEvent):
        """
        Log a structured event.
        
        Args:
            event: Event object (BaseEvent or subclass)
        """
        event_dict = event.model_dump(mode="json")
        event_dict = self._add_correlation_id(event_dict)
        
        # Map severity to logging level
        severity_map = {
            EventSeverity.DEBUG: logging.DEBUG,
            EventSeverity.INFO: logging.INFO,
            EventSeverity.WARNING: logging.WARNING,
            EventSeverity.ERROR: logging.ERROR,
            EventSeverity.CRITICAL: logging.CRITICAL,
        }
        level = severity_map.get(event.severity, logging.INFO)
        
        self.logger.log(level, json.dumps(event_dict))
    
    def log_recommendation_view(
        self,
        job_id: str,
        candidate_id: str,
        score: Optional[float] = None,
        rank: Optional[int] = None,
        context: Optional[str] = None,
    ):
        """Log a recommendation view event."""
        event = RecommendationEvent(
            event_type=EventType.RECOMMENDATION_VIEW,
            job_id=job_id,
            candidate_id=candidate_id,
            actor_id=candidate_id,
            score=score,
            rank=rank,
            context=context,
        )
        self.log_event(event)
    
    def log_recommendation_click(
        self,
        job_id: str,
        candidate_id: str,
        score: Optional[float] = None,
        rank: Optional[int] = None,
        context: Optional[str] = None,
    ):
        """Log a recommendation click event."""
        event = RecommendationEvent(
            event_type=EventType.RECOMMENDATION_CLICK,
            job_id=job_id,
            candidate_id=candidate_id,
            actor_id=candidate_id,
            score=score,
            rank=rank,
            context=context,
        )
        self.log_event(event)
    
    def log_application_submitted(
        self,
        application_id: str,
        job_id: str,
        candidate_id: str,
    ):
        """Log an application submission event."""
        event = ApplicationEvent(
            event_type=EventType.APPLICATION_SUBMITTED,
            application_id=application_id,
            job_id=job_id,
            candidate_id=candidate_id,
            actor_id=candidate_id,
            new_status="submitted",
        )
        self.log_event(event)
    
    def log_application_status_changed(
        self,
        application_id: str,
        job_id: str,
        candidate_id: str,
        previous_status: str,
        new_status: str,
        actor_id: Optional[str] = None,
    ):
        """Log an application status change event."""
        event = ApplicationEvent(
            event_type=EventType.APPLICATION_STATUS_CHANGED,
            application_id=application_id,
            job_id=job_id,
            candidate_id=candidate_id,
            actor_id=actor_id or candidate_id,
            previous_status=previous_status,
            new_status=new_status,
        )
        self.log_event(event)
    
    def log_inbox_action(
        self,
        employer_id: str,
        candidate_id: str,
        job_id: str,
        action: str,
        time_since_application: Optional[float] = None,
    ):
        """Log an employer inbox action event."""
        event_type_map = {
            "viewed": EventType.INBOX_CANDIDATE_VIEWED,
            "shortlisted": EventType.INBOX_CANDIDATE_SHORTLISTED,
            "rejected": EventType.INBOX_CANDIDATE_REJECTED,
        }
        event = InboxEvent(
            event_type=event_type_map.get(action, EventType.INBOX_CANDIDATE_VIEWED),
            employer_id=employer_id,
            candidate_id=candidate_id,
            job_id=job_id,
            actor_id=employer_id,
            action=action,
            time_since_application=time_since_application,
        )
        self.log_event(event)
    
    def log_feedback(
        self,
        user_id: str,
        feedback_type: str,
        target_type: str,
        target_id: str,
        feedback_text: Optional[str] = None,
    ):
        """Log a user feedback event."""
        event = FeedbackEvent(
            event_type=EventType.FEEDBACK_SUBMITTED,
            user_id=user_id,
            actor_id=user_id,
            feedback_type=feedback_type,
            target_type=target_type,
            target_id=target_id,
            feedback_text=feedback_text,
        )
        self.log_event(event)
    
    def log_resume_uploaded(
        self,
        candidate_id: str,
        resume_id: str,
        file_size: Optional[int] = None,
        file_type: Optional[str] = None,
    ):
        """Log a resume upload event."""
        event = ResumeEvent(
            event_type=EventType.RESUME_UPLOADED,
            candidate_id=candidate_id,
            actor_id=candidate_id,
            resume_id=resume_id,
            file_size=file_size,
            file_type=file_type,
        )
        self.log_event(event)
    
    def log_resume_parsed(
        self,
        candidate_id: str,
        resume_id: str,
        parsing_duration: Optional[float] = None,
        success: bool = True,
    ):
        """Log a resume parsing event."""
        event = ResumeEvent(
            event_type=EventType.RESUME_PARSED,
            candidate_id=candidate_id,
            resume_id=resume_id,
            parsing_duration=parsing_duration,
            success=success,
            severity=EventSeverity.INFO if success else EventSeverity.WARNING,
        )
        self.log_event(event)
    
    def log_job_posted(
        self,
        job_id: str,
        employer_id: str,
        job_title: Optional[str] = None,
    ):
        """Log a job posting event."""
        event = JobEvent(
            event_type=EventType.JOB_POSTED,
            job_id=job_id,
            employer_id=employer_id,
            actor_id=employer_id,
            job_title=job_title,
        )
        self.log_event(event)
    
    def log_job_indexed(
        self,
        job_id: str,
        employer_id: str,
        indexing_duration: Optional[float] = None,
        success: bool = True,
    ):
        """Log a job indexing event."""
        event = JobEvent(
            event_type=EventType.JOB_INDEXED,
            job_id=job_id,
            employer_id=employer_id,
            indexing_duration=indexing_duration,
            success=success,
            severity=EventSeverity.INFO if success else EventSeverity.WARNING,
        )
        self.log_event(event)
    
    def log_error(
        self,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        request_path: Optional[str] = None,
        request_method: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        """Log an error event."""
        event = ErrorEvent(
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            request_path=request_path,
            request_method=request_method,
            user_id=user_id,
            actor_id=user_id,
        )
        self.log_event(event)
    
    def log_system_event(
        self,
        event_type: EventType,
        service_name: str,
        environment: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Log a system event."""
        event = SystemEvent(
            event_type=event_type,
            service_name=service_name,
            environment=environment,
            version=version,
        )
        self.log_event(event)


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        # If the message is already JSON, use it directly
        try:
            message = json.loads(record.getMessage())
            if isinstance(message, dict):
                return json.dumps(message)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Otherwise, create a structured log entry
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        if hasattr(record, "correlation_id"):
            log_obj["correlation_id"] = record.correlation_id
        
        return json.dumps(log_obj)


# Global logger instance
logger = StructuredLogger()


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """
    Set correlation ID for the current context.
    
    Args:
        correlation_id: Correlation ID to set, or None to generate a new one
        
    Returns:
        The correlation ID that was set
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    correlation_id_var.set(correlation_id)
    return correlation_id


def get_correlation_id() -> Optional[str]:
    """Get the correlation ID for the current context."""
    return correlation_id_var.get()


def clear_correlation_id():
    """Clear the correlation ID for the current context."""
    correlation_id_var.set(None)
