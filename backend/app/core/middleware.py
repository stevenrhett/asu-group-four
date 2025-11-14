"""
Middleware for request tracking and logging.
"""
import time
import traceback
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.services.logging import logger, set_correlation_id, clear_correlation_id


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured logging with correlation IDs.
    
    Automatically tracks requests with correlation IDs and logs
    request/response metadata and errors.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with correlation ID tracking."""
        # Generate or extract correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        correlation_id = set_correlation_id(correlation_id)
        
        # Track request start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log request/response
            self._log_request(request, response, duration, correlation_id)
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
        
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log error
            self._log_error(request, e, duration, correlation_id)
            
            # Re-raise exception to be handled by FastAPI error handlers
            raise
        
        finally:
            # Clear correlation ID from context
            clear_correlation_id()
    
    def _log_request(
        self,
        request: Request,
        response: Response,
        duration: float,
        correlation_id: str,
    ):
        """Log request/response details."""
        # Extract user ID if available
        user_id = None
        if hasattr(request.state, "user"):
            user_id = str(request.state.user.id)
        
        # Build metadata
        metadata = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": duration,
            "correlation_id": correlation_id,
            "user_agent": request.headers.get("user-agent"),
        }
        
        if user_id:
            metadata["user_id"] = user_id
        
        # Log based on status code
        if response.status_code >= 500:
            from app.schemas.events import BaseEvent, EventType, EventSeverity
            event = BaseEvent(
                event_type=EventType.ERROR_OCCURRED,
                severity=EventSeverity.ERROR,
                correlation_id=correlation_id,
                actor_id=user_id,
                metadata=metadata,
            )
            logger.log_event(event)
        elif response.status_code >= 400:
            from app.schemas.events import BaseEvent, EventType, EventSeverity
            event = BaseEvent(
                event_type=EventType.ERROR_OCCURRED,
                severity=EventSeverity.WARNING,
                correlation_id=correlation_id,
                actor_id=user_id,
                metadata=metadata,
            )
            logger.log_event(event)
    
    def _log_error(
        self,
        request: Request,
        error: Exception,
        duration: float,
        correlation_id: str,
    ):
        """Log error details."""
        # Extract user ID if available
        user_id = None
        if hasattr(request.state, "user"):
            user_id = str(request.state.user.id)
        
        # Get stack trace
        stack_trace = "".join(traceback.format_exception(
            type(error), error, error.__traceback__
        ))
        
        # Log error event
        logger.log_error(
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=stack_trace,
            request_path=request.url.path,
            request_method=request.method,
            user_id=user_id,
        )


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting performance metrics.
    
    Tracks request counts, response times, and status codes
    for monitoring and alerting.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_count = 0
        self.error_count = 0
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track request metrics."""
        self.request_count += 1
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            if response.status_code >= 400:
                self.error_count += 1
            
            # Add timing header
            duration = time.time() - start_time
            response.headers["X-Response-Time"] = f"{duration:.4f}"
            
            return response
        
        except Exception as e:
            self.error_count += 1
            raise
