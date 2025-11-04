"""
Tests for event schema and logging service.
"""
import pytest
from datetime import datetime
from app.schemas.events import (
    EventType,
    EventSeverity,
    BaseEvent,
    RecommendationEvent,
    ApplicationEvent,
    InboxEvent,
    ErrorEvent,
)
from app.services.logging import (
    StructuredLogger,
    set_correlation_id,
    get_correlation_id,
    clear_correlation_id,
)


class TestEventSchemas:
    """Test event schema definitions."""
    
    def test_base_event_creation(self):
        """Test creating a base event."""
        event = BaseEvent(
            event_type=EventType.SYSTEM_STARTUP,
            severity=EventSeverity.INFO,
        )
        
        assert event.event_type == EventType.SYSTEM_STARTUP
        assert event.severity == EventSeverity.INFO
        assert isinstance(event.timestamp, datetime)
        assert event.metadata == {}
    
    def test_recommendation_event(self):
        """Test recommendation event schema."""
        event = RecommendationEvent(
            event_type=EventType.RECOMMENDATION_VIEW,
            job_id="job_123",
            candidate_id="user_456",
            score=0.85,
            rank=1,
            context="homepage",
        )
        
        assert event.job_id == "job_123"
        assert event.candidate_id == "user_456"
        assert event.score == 0.85
        assert event.rank == 1
        assert event.context == "homepage"
    
    def test_application_event(self):
        """Test application event schema."""
        event = ApplicationEvent(
            event_type=EventType.APPLICATION_STATUS_CHANGED,
            application_id="app_789",
            job_id="job_123",
            candidate_id="user_456",
            previous_status="submitted",
            new_status="shortlisted",
        )
        
        assert event.application_id == "app_789"
        assert event.previous_status == "submitted"
        assert event.new_status == "shortlisted"
    
    def test_error_event_defaults(self):
        """Test error event default values."""
        event = ErrorEvent(
            error_type="ValueError",
            error_message="Invalid input",
        )
        
        assert event.severity == EventSeverity.ERROR
        assert event.event_type == EventType.ERROR_OCCURRED


class TestStructuredLogger:
    """Test structured logging service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.logger = StructuredLogger(name="test_logger")
    
    def test_log_recommendation_view(self):
        """Test logging a recommendation view."""
        # Should not raise an exception
        self.logger.log_recommendation_view(
            job_id="job_123",
            candidate_id="user_456",
            score=0.85,
            rank=1,
            context="homepage",
        )
    
    def test_log_recommendation_click(self):
        """Test logging a recommendation click."""
        self.logger.log_recommendation_click(
            job_id="job_123",
            candidate_id="user_456",
            score=0.85,
            rank=1,
        )
    
    def test_log_application_submitted(self):
        """Test logging an application submission."""
        self.logger.log_application_submitted(
            application_id="app_789",
            job_id="job_123",
            candidate_id="user_456",
        )
    
    def test_log_application_status_changed(self):
        """Test logging an application status change."""
        self.logger.log_application_status_changed(
            application_id="app_789",
            job_id="job_123",
            candidate_id="user_456",
            previous_status="submitted",
            new_status="shortlisted",
            actor_id="employer_999",
        )
    
    def test_log_inbox_action(self):
        """Test logging an inbox action."""
        self.logger.log_inbox_action(
            employer_id="employer_999",
            candidate_id="user_456",
            job_id="job_123",
            action="shortlisted",
            time_since_application=3600.0,
        )
    
    def test_log_error(self):
        """Test logging an error."""
        self.logger.log_error(
            error_type="ValueError",
            error_message="Invalid input",
            stack_trace="Traceback...",
            request_path="/api/v1/jobs",
            request_method="POST",
            user_id="user_456",
        )


class TestCorrelationID:
    """Test correlation ID tracking."""
    
    def setup_method(self):
        """Clear correlation ID before each test."""
        clear_correlation_id()
    
    def test_set_and_get_correlation_id(self):
        """Test setting and getting correlation ID."""
        correlation_id = set_correlation_id("test-correlation-id")
        
        assert correlation_id == "test-correlation-id"
        assert get_correlation_id() == "test-correlation-id"
    
    def test_auto_generate_correlation_id(self):
        """Test auto-generating correlation ID."""
        correlation_id = set_correlation_id()
        
        assert correlation_id is not None
        assert len(correlation_id) > 0
        assert get_correlation_id() == correlation_id
    
    def test_clear_correlation_id(self):
        """Test clearing correlation ID."""
        set_correlation_id("test-id")
        clear_correlation_id()
        
        assert get_correlation_id() is None
    
    def test_correlation_id_in_event(self):
        """Test correlation ID is added to events."""
        correlation_id = set_correlation_id("test-correlation-id")
        
        logger = StructuredLogger(name="test_logger")
        
        # Log an event - correlation ID should be automatically added
        # This test verifies the mechanism exists; actual verification
        # would require capturing log output
        logger.log_recommendation_view(
            job_id="job_123",
            candidate_id="user_456",
        )
        
        clear_correlation_id()


class TestEventSerialization:
    """Test event serialization to JSON."""
    
    def test_base_event_serialization(self):
        """Test serializing base event to dict."""
        event = BaseEvent(
            event_type=EventType.SYSTEM_STARTUP,
            correlation_id="test-id",
            metadata={"key": "value"},
        )
        
        event_dict = event.model_dump(mode="json")
        
        assert event_dict["event_type"] == "system.startup"
        assert event_dict["correlation_id"] == "test-id"
        assert event_dict["metadata"] == {"key": "value"}
        assert "timestamp" in event_dict
    
    def test_recommendation_event_serialization(self):
        """Test serializing recommendation event."""
        event = RecommendationEvent(
            event_type=EventType.RECOMMENDATION_VIEW,
            job_id="job_123",
            candidate_id="user_456",
            score=0.85,
        )
        
        event_dict = event.model_dump(mode="json")
        
        assert event_dict["job_id"] == "job_123"
        assert event_dict["candidate_id"] == "user_456"
        assert event_dict["score"] == 0.85
