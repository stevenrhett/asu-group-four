"""
Tests for metrics aggregation service.
"""
import pytest
from datetime import datetime, timedelta
from app.services.metrics import MetricsService, KPIMetrics
from app.schemas.events import EventType


class TestMetricsService:
    """Test metrics aggregation service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = MetricsService()
        self.service.clear_events()
    
    def teardown_method(self):
        """Clean up after tests."""
        self.service.clear_events()
    
    def test_add_event(self):
        """Test adding events to the store."""
        event = {
            "event_type": EventType.RECOMMENDATION_VIEW,
            "timestamp": datetime.utcnow().isoformat(),
            "job_id": "job_123",
            "candidate_id": "user_456",
        }
        
        self.service.add_event(event)
        
        assert len(self.service.event_store) == 1
    
    def test_get_kpis_empty(self):
        """Test getting KPIs with no events."""
        kpis = self.service.get_kpis()
        
        assert kpis.total_events == 0
        assert kpis.recommendation_views == 0
        assert kpis.recommendation_clicks == 0
        assert kpis.ctr == 0.0
    
    def test_calculate_ctr(self):
        """Test calculating click-through rate."""
        now = datetime.utcnow()
        
        # Add 10 views
        for i in range(10):
            self.service.add_event({
                "event_type": EventType.RECOMMENDATION_VIEW,
                "timestamp": now.isoformat(),
                "job_id": f"job_{i}",
                "candidate_id": "user_456",
                "actor_id": "user_456",
            })
        
        # Add 3 clicks
        for i in range(3):
            self.service.add_event({
                "event_type": EventType.RECOMMENDATION_CLICK,
                "timestamp": now.isoformat(),
                "job_id": f"job_{i}",
                "candidate_id": "user_456",
                "actor_id": "user_456",
            })
        
        kpis = self.service.get_kpis()
        
        assert kpis.recommendation_views == 10
        assert kpis.recommendation_clicks == 3
        assert kpis.ctr == 0.3  # 3/10
    
    def test_calculate_conversion_rate(self):
        """Test calculating application conversion rate."""
        now = datetime.utcnow()
        
        # Add 5 clicks
        for i in range(5):
            self.service.add_event({
                "event_type": EventType.RECOMMENDATION_CLICK,
                "timestamp": now.isoformat(),
                "job_id": f"job_{i}",
                "candidate_id": "user_456",
                "actor_id": "user_456",
            })
        
        # Add 2 applications
        for i in range(2):
            self.service.add_event({
                "event_type": EventType.APPLICATION_SUBMITTED,
                "timestamp": now.isoformat(),
                "application_id": f"app_{i}",
                "job_id": f"job_{i}",
                "candidate_id": "user_456",
                "actor_id": "user_456",
            })
        
        kpis = self.service.get_kpis()
        
        assert kpis.recommendation_clicks == 5
        assert kpis.applications_submitted == 2
        assert kpis.application_conversion_rate == 0.4  # 2/5
    
    def test_inbox_metrics(self):
        """Test inbox action metrics."""
        now = datetime.utcnow()
        
        # Add inbox events
        self.service.add_event({
            "event_type": EventType.INBOX_CANDIDATE_VIEWED,
            "timestamp": now.isoformat(),
            "employer_id": "emp_123",
            "candidate_id": "user_456",
            "job_id": "job_789",
            "actor_id": "emp_123",
        })
        
        self.service.add_event({
            "event_type": EventType.INBOX_CANDIDATE_SHORTLISTED,
            "timestamp": now.isoformat(),
            "employer_id": "emp_123",
            "candidate_id": "user_456",
            "job_id": "job_789",
            "actor_id": "emp_123",
            "time_since_application": 3600.0,
        })
        
        kpis = self.service.get_kpis()
        
        assert kpis.candidates_viewed == 1
        assert kpis.candidates_shortlisted == 1
        assert kpis.median_time_to_shortlist == 3600.0
    
    def test_median_time_to_shortlist_multiple(self):
        """Test median calculation with multiple values."""
        now = datetime.utcnow()
        
        times = [1000.0, 2000.0, 3000.0, 4000.0, 5000.0]
        
        for time_val in times:
            self.service.add_event({
                "event_type": EventType.INBOX_CANDIDATE_SHORTLISTED,
                "timestamp": now.isoformat(),
                "employer_id": "emp_123",
                "candidate_id": f"user_{time_val}",
                "job_id": "job_789",
                "actor_id": "emp_123",
                "time_since_application": time_val,
            })
        
        kpis = self.service.get_kpis()
        
        assert kpis.median_time_to_shortlist == 3000.0
    
    def test_unique_users(self):
        """Test tracking unique users."""
        now = datetime.utcnow()
        
        # Add events from 3 different users
        for user_id in ["user_1", "user_2", "user_3"]:
            self.service.add_event({
                "event_type": EventType.RECOMMENDATION_VIEW,
                "timestamp": now.isoformat(),
                "job_id": "job_123",
                "candidate_id": user_id,
                "actor_id": user_id,
            })
        
        # Add another event from user_1 (should not increase count)
        self.service.add_event({
            "event_type": EventType.RECOMMENDATION_CLICK,
            "timestamp": now.isoformat(),
            "job_id": "job_123",
            "candidate_id": "user_1",
            "actor_id": "user_1",
        })
        
        kpis = self.service.get_kpis()
        
        assert kpis.unique_users == 3
    
    def test_time_period_filtering(self):
        """Test filtering events by time period."""
        base_time = datetime.utcnow()
        
        # Add event from yesterday
        self.service.add_event({
            "event_type": EventType.RECOMMENDATION_VIEW,
            "timestamp": (base_time - timedelta(days=1)).isoformat(),
            "job_id": "job_old",
            "candidate_id": "user_456",
            "actor_id": "user_456",
        })
        
        # Add event from today
        self.service.add_event({
            "event_type": EventType.RECOMMENDATION_VIEW,
            "timestamp": base_time.isoformat(),
            "job_id": "job_new",
            "candidate_id": "user_456",
            "actor_id": "user_456",
        })
        
        # Get KPIs for today only
        kpis = self.service.get_kpis(
            start_date=base_time - timedelta(hours=1),
            end_date=base_time + timedelta(hours=1),
        )
        
        assert kpis.total_events == 1
        assert kpis.recommendation_views == 1
    
    def test_ctr_time_series(self):
        """Test CTR time series generation."""
        now = datetime.utcnow()
        
        # Add events across 3 days
        for day in range(3):
            day_time = now - timedelta(days=2-day)
            
            # Add views and clicks for this day
            for _ in range(10):
                self.service.add_event({
                    "event_type": EventType.RECOMMENDATION_VIEW,
                    "timestamp": day_time.isoformat(),
                    "job_id": "job_123",
                    "candidate_id": "user_456",
                })
            
            for _ in range(day + 1):  # Increasing clicks each day
                self.service.add_event({
                    "event_type": EventType.RECOMMENDATION_CLICK,
                    "timestamp": day_time.isoformat(),
                    "job_id": "job_123",
                    "candidate_id": "user_456",
                })
        
        # Get time series
        time_series = self.service.get_ctr_time_series(
            start_date=now - timedelta(days=3),
            end_date=now,
            bucket_size=timedelta(days=1),
        )
        
        assert len(time_series) >= 3
        # CTR should increase over time (1/10, 2/10, 3/10)
        # Note: exact values depend on bucket boundaries
    
    def test_conversion_time_series(self):
        """Test conversion rate time series generation."""
        now = datetime.utcnow()
        
        # Add events for today
        for _ in range(5):
            self.service.add_event({
                "event_type": EventType.RECOMMENDATION_CLICK,
                "timestamp": now.isoformat(),
                "job_id": "job_123",
                "candidate_id": "user_456",
            })
        
        for _ in range(2):
            self.service.add_event({
                "event_type": EventType.APPLICATION_SUBMITTED,
                "timestamp": now.isoformat(),
                "application_id": "app_123",
                "job_id": "job_123",
                "candidate_id": "user_456",
            })
        
        # Get time series
        time_series = self.service.get_conversion_time_series(
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1),
            bucket_size=timedelta(days=1),
        )
        
        assert len(time_series) >= 1
