"""
Metrics aggregation service for KPI tracking and dashboard.

Aggregates event data to calculate key performance indicators:
- Click-through rate (CTR) on recommendations
- Application conversion rate
- Time-to-shortlist metrics
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

from app.schemas.events import EventType


class KPIMetrics(BaseModel):
    """Container for KPI metrics."""
    
    period_start: datetime
    period_end: datetime
    
    # Recommendation metrics
    recommendation_views: int = 0
    recommendation_clicks: int = 0
    ctr: float = 0.0  # Click-through rate
    
    # Application metrics
    applications_submitted: int = 0
    applications_from_recommendations: int = 0
    application_conversion_rate: float = 0.0
    
    # Inbox metrics
    candidates_viewed: int = 0
    candidates_shortlisted: int = 0
    candidates_rejected: int = 0
    median_time_to_shortlist: Optional[float] = None  # seconds
    
    # Overall engagement
    total_events: int = 0
    unique_users: int = 0


class TimeSeriesMetric(BaseModel):
    """Time series data point for metrics."""
    
    timestamp: datetime
    value: float
    label: str


class MetricsService:
    """
    Service for aggregating and calculating metrics from event logs.
    
    In MVP, this reads from a simple event store. In production,
    this would integrate with a time-series database or analytics platform.
    """
    
    def __init__(self, event_store: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize metrics service.
        
        Args:
            event_store: In-memory event store (for MVP). In production,
                        this would be a database connection.
        """
        self.event_store = event_store or []
    
    def add_event(self, event_dict: Dict[str, Any]):
        """
        Add an event to the store.
        
        Args:
            event_dict: Event data as dictionary
        """
        self.event_store.append(event_dict)
    
    def get_kpis(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> KPIMetrics:
        """
        Calculate KPI metrics for a time period.
        
        Args:
            start_date: Start of period (default: 30 days ago)
            end_date: End of period (default: now)
            
        Returns:
            KPIMetrics object with calculated metrics
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Filter events by time period
        period_events = [
            e for e in self.event_store
            if self._parse_timestamp(e.get("timestamp", "")) >= start_date
            and self._parse_timestamp(e.get("timestamp", "")) <= end_date
        ]
        
        # Initialize metrics
        metrics = KPIMetrics(
            period_start=start_date,
            period_end=end_date,
        )
        
        # Track unique users
        unique_users = set()
        
        # Track time to shortlist
        application_times = {}  # application_id -> submitted_time
        shortlist_times = []
        
        # Process events
        for event in period_events:
            event_type = event.get("event_type")
            
            # Track unique users
            if event.get("actor_id"):
                unique_users.add(event.get("actor_id"))
            
            # Recommendation metrics
            if event_type == EventType.RECOMMENDATION_VIEW:
                metrics.recommendation_views += 1
            elif event_type == EventType.RECOMMENDATION_CLICK:
                metrics.recommendation_clicks += 1
            
            # Application metrics
            elif event_type == EventType.APPLICATION_SUBMITTED:
                metrics.applications_submitted += 1
                application_id = event.get("application_id")
                if application_id:
                    application_times[application_id] = self._parse_timestamp(
                        event.get("timestamp", "")
                    )
            
            # Inbox metrics
            elif event_type == EventType.INBOX_CANDIDATE_VIEWED:
                metrics.candidates_viewed += 1
            elif event_type == EventType.INBOX_CANDIDATE_SHORTLISTED:
                metrics.candidates_shortlisted += 1
                # Calculate time to shortlist if available
                if event.get("time_since_application"):
                    shortlist_times.append(event.get("time_since_application"))
            elif event_type == EventType.INBOX_CANDIDATE_REJECTED:
                metrics.candidates_rejected += 1
        
        # Calculate derived metrics
        metrics.total_events = len(period_events)
        metrics.unique_users = len(unique_users)
        
        # CTR = clicks / views
        if metrics.recommendation_views > 0:
            metrics.ctr = metrics.recommendation_clicks / metrics.recommendation_views
        
        # Conversion rate = applications / clicks
        if metrics.recommendation_clicks > 0:
            metrics.application_conversion_rate = (
                metrics.applications_submitted / metrics.recommendation_clicks
            )
        
        # Median time to shortlist
        if shortlist_times:
            shortlist_times.sort()
            mid = len(shortlist_times) // 2
            if len(shortlist_times) % 2 == 0:
                metrics.median_time_to_shortlist = (
                    shortlist_times[mid - 1] + shortlist_times[mid]
                ) / 2
            else:
                metrics.median_time_to_shortlist = shortlist_times[mid]
        
        return metrics
    
    def get_ctr_time_series(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bucket_size: timedelta = timedelta(days=1),
    ) -> List[TimeSeriesMetric]:
        """
        Get CTR over time as a time series.
        
        Args:
            start_date: Start of period
            end_date: End of period
            bucket_size: Time bucket size for aggregation
            
        Returns:
            List of time series data points
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Create time buckets
        buckets = []
        current = start_date
        while current < end_date:
            next_bucket = current + bucket_size
            buckets.append((current, next_bucket))
            current = next_bucket
        
        # Calculate CTR for each bucket
        time_series = []
        for bucket_start, bucket_end in buckets:
            bucket_events = [
                e for e in self.event_store
                if bucket_start <= self._parse_timestamp(e.get("timestamp", "")) < bucket_end
            ]
            
            views = sum(
                1 for e in bucket_events
                if e.get("event_type") == EventType.RECOMMENDATION_VIEW
            )
            clicks = sum(
                1 for e in bucket_events
                if e.get("event_type") == EventType.RECOMMENDATION_CLICK
            )
            
            ctr = clicks / views if views > 0 else 0.0
            
            time_series.append(TimeSeriesMetric(
                timestamp=bucket_start,
                value=ctr,
                label="CTR",
            ))
        
        return time_series
    
    def get_conversion_time_series(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bucket_size: timedelta = timedelta(days=1),
    ) -> List[TimeSeriesMetric]:
        """
        Get application conversion rate over time.
        
        Args:
            start_date: Start of period
            end_date: End of period
            bucket_size: Time bucket size for aggregation
            
        Returns:
            List of time series data points
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Create time buckets
        buckets = []
        current = start_date
        while current < end_date:
            next_bucket = current + bucket_size
            buckets.append((current, next_bucket))
            current = next_bucket
        
        # Calculate conversion for each bucket
        time_series = []
        for bucket_start, bucket_end in buckets:
            bucket_events = [
                e for e in self.event_store
                if bucket_start <= self._parse_timestamp(e.get("timestamp", "")) < bucket_end
            ]
            
            clicks = sum(
                1 for e in bucket_events
                if e.get("event_type") == EventType.RECOMMENDATION_CLICK
            )
            applications = sum(
                1 for e in bucket_events
                if e.get("event_type") == EventType.APPLICATION_SUBMITTED
            )
            
            conversion = applications / clicks if clicks > 0 else 0.0
            
            time_series.append(TimeSeriesMetric(
                timestamp=bucket_start,
                value=conversion,
                label="Conversion Rate",
            ))
        
        return time_series
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse ISO timestamp string to datetime."""
        try:
            return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.min
    
    def clear_events(self):
        """Clear all events from the store (for testing)."""
        self.event_store.clear()


# Global metrics service instance
metrics_service = MetricsService()
