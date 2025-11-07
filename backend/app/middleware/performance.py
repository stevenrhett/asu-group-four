"""
Performance monitoring middleware for latency and error tracking (ST-013).

Tracks request latency (P50, P95, P99) and error rates per endpoint
to ensure SLA compliance.
"""
import time
from typing import Callable, Dict, List
from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.services.logging import logger as event_logger
from app.schemas.events import BaseEvent, EventType, EventSeverity


class LatencyTracker:
    """
    Tracks latency metrics for endpoints.
    
    Maintains sliding window of latency measurements and calculates
    percentiles (P50, P95, P99).
    """
    
    def __init__(self, window_size: int = 1000):
        """
        Initialize latency tracker.
        
        Args:
            window_size: Maximum number of measurements to keep per endpoint
        """
        self.latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.request_counts: Dict[str, int] = defaultdict(int)
    
    def add_measurement(self, endpoint: str, latency_ms: float, status_code: int):
        """
        Add a latency measurement for an endpoint.
        
        Args:
            endpoint: The endpoint path
            latency_ms: Latency in milliseconds
            status_code: HTTP status code
        """
        self.latencies[endpoint].append(latency_ms)
        self.request_counts[endpoint] += 1
        
        if status_code >= 400:
            self.error_counts[endpoint] += 1
    
    def get_percentile(self, endpoint: str, percentile: int) -> float:
        """
        Calculate percentile latency for an endpoint.
        
        Args:
            endpoint: The endpoint path
            percentile: Percentile to calculate (e.g., 50, 95, 99)
            
        Returns:
            Percentile latency in milliseconds, or 0 if no data
        """
        if endpoint not in self.latencies or not self.latencies[endpoint]:
            return 0.0
        
        sorted_latencies = sorted(self.latencies[endpoint])
        index = int(len(sorted_latencies) * percentile / 100)
        if index >= len(sorted_latencies):
            index = len(sorted_latencies) - 1
        
        return sorted_latencies[index]
    
    def get_error_rate(self, endpoint: str) -> float:
        """
        Calculate error rate for an endpoint.
        
        Args:
            endpoint: The endpoint path
            
        Returns:
            Error rate as a decimal (0.0 to 1.0)
        """
        if self.request_counts[endpoint] == 0:
            return 0.0
        
        return self.error_counts[endpoint] / self.request_counts[endpoint]
    
    def get_metrics(self, endpoint: str) -> Dict:
        """
        Get all metrics for an endpoint.
        
        Args:
            endpoint: The endpoint path
            
        Returns:
            Dictionary with latency percentiles and error rate
        """
        return {
            "endpoint": endpoint,
            "request_count": self.request_counts[endpoint],
            "error_count": self.error_counts[endpoint],
            "error_rate": self.get_error_rate(endpoint),
            "latency_p50_ms": self.get_percentile(endpoint, 50),
            "latency_p95_ms": self.get_percentile(endpoint, 95),
            "latency_p99_ms": self.get_percentile(endpoint, 99),
        }
    
    def get_all_metrics(self) -> List[Dict]:
        """
        Get metrics for all tracked endpoints.
        
        Returns:
            List of metrics dictionaries
        """
        return [
            self.get_metrics(endpoint)
            for endpoint in self.request_counts.keys()
        ]


# Global latency tracker instance
latency_tracker = LatencyTracker(window_size=1000)


# SLA Budgets per endpoint (in milliseconds)
LATENCY_BUDGETS = {
    "/api/v1/auth/register": {"p95": 1000, "p99": 2000},
    "/api/v1/auth/login": {"p95": 500, "p99": 1000},
    "/api/v1/jobs": {"p95": 200, "p99": 500},
    "/api/v1/recommendations": {"p95": 1000, "p99": 2000},
    "/api/v1/applications": {"p95": 500, "p99": 1000},
}

# Error rate budgets (as decimals, e.g., 0.01 = 1%)
ERROR_RATE_BUDGET = 0.01  # 1% error budget


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track request latency and error rates.
    
    Measures request duration and tracks metrics per endpoint.
    Logs warnings when endpoints exceed SLA budgets.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and track performance metrics.
        
        Args:
            request: The incoming request
            call_next: Next middleware/handler in chain
            
        Returns:
            The response
        """
        # Start timing
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            # Track errors
            status_code = 500
            latency_ms = (time.time() - start_time) * 1000
            
            # Log error event
            event_logger.log_error(
                error_type=type(e).__name__,
                error_message=str(e),
                request_path=request.url.path,
                request_method=request.method,
            )
            
            raise
        finally:
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Normalize endpoint (remove IDs and query params)
            endpoint = self._normalize_endpoint(request.url.path)
            
            # Track metrics
            latency_tracker.add_measurement(endpoint, latency_ms, status_code)
            
            # Check SLA budgets
            self._check_sla_budgets(endpoint, latency_ms, status_code)
        
        return response
    
    def _normalize_endpoint(self, path: str) -> str:
        """
        Normalize endpoint path for metrics grouping.
        
        Removes UUIDs and IDs from paths to group similar endpoints.
        
        Args:
            path: The request path
            
        Returns:
            Normalized path
        """
        import re
        
        # Replace UUIDs and object IDs with placeholder
        path = re.sub(r'/[0-9a-f]{24}', '/:id', path)  # MongoDB ObjectIds
        path = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/:id', path)  # UUIDs
        path = re.sub(r'/\d+', '/:id', path)  # Numeric IDs
        
        return path
    
    def _check_sla_budgets(self, endpoint: str, latency_ms: float, status_code: int):
        """
        Check if request exceeds SLA budgets and log if necessary.
        
        Args:
            endpoint: The normalized endpoint path
            latency_ms: Request latency in milliseconds
            status_code: HTTP status code
        """
        metrics = latency_tracker.get_metrics(endpoint)
        
        # Check latency budget
        if endpoint in LATENCY_BUDGETS:
            budget = LATENCY_BUDGETS[endpoint]
            
            if metrics["latency_p95_ms"] > budget["p95"]:
                event_logger.log_event(
                    BaseEvent(
                        event_type=EventType.SLA_LATENCY_BUDGET_EXCEEDED,
                        severity=EventSeverity.WARNING,
                        metadata={
                            "endpoint": endpoint,
                            "p95_ms": metrics["latency_p95_ms"],
                            "budget_p95_ms": budget["p95"],
                            "current_latency_ms": latency_ms
                        }
                    )
                )
            
            if metrics["latency_p99_ms"] > budget["p99"]:
                event_logger.log_event(
                    BaseEvent(
                        event_type=EventType.SLA_LATENCY_BUDGET_EXCEEDED,
                        severity=EventSeverity.CRITICAL,
                        metadata={
                            "endpoint": endpoint,
                            "p99_ms": metrics["latency_p99_ms"],
                            "budget_p99_ms": budget["p99"],
                            "current_latency_ms": latency_ms
                        }
                    )
                )
        
        # Check error rate budget
        if metrics["error_rate"] > ERROR_RATE_BUDGET:
            event_logger.log_event(
                BaseEvent(
                    event_type=EventType.SLA_ERROR_BUDGET_EXCEEDED,
                    severity=EventSeverity.CRITICAL,
                    metadata={
                        "endpoint": endpoint,
                        "error_rate": metrics["error_rate"],
                        "error_budget": ERROR_RATE_BUDGET,
                        "error_count": metrics["error_count"],
                        "request_count": metrics["request_count"]
                    }
                )
            )


def get_latency_metrics() -> List[Dict]:
    """
    Get current latency and error metrics for all endpoints.
    
    Returns:
        List of metrics dictionaries
    """
    return latency_tracker.get_all_metrics()


def get_endpoint_metrics(endpoint: str) -> Dict:
    """
    Get metrics for a specific endpoint.
    
    Args:
        endpoint: The endpoint path
        
    Returns:
        Metrics dictionary
    """
    return latency_tracker.get_metrics(endpoint)
