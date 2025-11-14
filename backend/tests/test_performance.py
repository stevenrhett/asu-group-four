"""
Tests for performance monitoring and SLA budgets (ST-013).

Tests latency tracking, error rate monitoring, and SLA budget compliance.
"""
import pytest
from app.middleware.performance import LatencyTracker, LATENCY_BUDGETS, ERROR_RATE_BUDGET


class TestLatencyTracker:
    """Test the latency tracking functionality."""
    
    def test_add_measurement(self):
        """Test adding latency measurements."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 150.5, 200)
        tracker.add_measurement("/api/v1/jobs", 200.3, 200)
        tracker.add_measurement("/api/v1/jobs", 175.8, 200)
        
        assert tracker.request_counts["/api/v1/jobs"] == 3
        assert tracker.error_counts["/api/v1/jobs"] == 0
    
    def test_error_tracking(self):
        """Test that errors are tracked correctly."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100.0, 200)
        tracker.add_measurement("/api/v1/jobs", 150.0, 404)
        tracker.add_measurement("/api/v1/jobs", 200.0, 500)
        
        assert tracker.request_counts["/api/v1/jobs"] == 3
        assert tracker.error_counts["/api/v1/jobs"] == 2
        assert tracker.get_error_rate("/api/v1/jobs") == 2/3
    
    def test_percentile_calculation_p50(self):
        """Test P50 (median) calculation."""
        tracker = LatencyTracker(window_size=100)
        
        # Add measurements: 100, 200, 300, 400, 500
        for latency in [100, 200, 300, 400, 500]:
            tracker.add_measurement("/api/v1/jobs", latency, 200)
        
        p50 = tracker.get_percentile("/api/v1/jobs", 50)
        assert p50 == 300  # Median of [100, 200, 300, 400, 500]
    
    def test_percentile_calculation_p95(self):
        """Test P95 calculation."""
        tracker = LatencyTracker(window_size=100)
        
        # Add 100 measurements from 1 to 100
        for i in range(1, 101):
            tracker.add_measurement("/api/v1/jobs", i, 200)
        
        p95 = tracker.get_percentile("/api/v1/jobs", 95)
        # P95 of 1-100 should be around 95 or 96 depending on rounding
        assert p95 >= 95 and p95 <= 96
    
    def test_percentile_calculation_p99(self):
        """Test P99 calculation."""
        tracker = LatencyTracker(window_size=100)
        
        # Add 100 measurements from 1 to 100
        for i in range(1, 101):
            tracker.add_measurement("/api/v1/jobs", i, 200)
        
        p99 = tracker.get_percentile("/api/v1/jobs", 99)
        # P99 of 1-100 should be around 99 or 100 depending on rounding
        assert p99 >= 99 and p99 <= 100
    
    def test_percentile_empty_data(self):
        """Test percentile calculation with no data."""
        tracker = LatencyTracker(window_size=100)
        
        p95 = tracker.get_percentile("/api/v1/jobs", 95)
        assert p95 == 0.0
    
    def test_error_rate_zero_requests(self):
        """Test error rate with zero requests."""
        tracker = LatencyTracker(window_size=100)
        
        error_rate = tracker.get_error_rate("/api/v1/jobs")
        assert error_rate == 0.0
    
    def test_get_metrics(self):
        """Test getting all metrics for an endpoint."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100, 200)
        tracker.add_measurement("/api/v1/jobs", 200, 200)
        tracker.add_measurement("/api/v1/jobs", 300, 404)
        
        metrics = tracker.get_metrics("/api/v1/jobs")
        
        assert metrics["endpoint"] == "/api/v1/jobs"
        assert metrics["request_count"] == 3
        assert metrics["error_count"] == 1
        assert metrics["error_rate"] == 1/3
        assert metrics["latency_p50_ms"] == 200
        assert "latency_p95_ms" in metrics
        assert "latency_p99_ms" in metrics
    
    def test_get_all_metrics(self):
        """Test getting metrics for all endpoints."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100, 200)
        tracker.add_measurement("/api/v1/auth/login", 50, 200)
        tracker.add_measurement("/api/v1/applications", 200, 200)
        
        all_metrics = tracker.get_all_metrics()
        
        assert len(all_metrics) == 3
        endpoints = [m["endpoint"] for m in all_metrics]
        assert "/api/v1/jobs" in endpoints
        assert "/api/v1/auth/login" in endpoints
        assert "/api/v1/applications" in endpoints


class TestWindowSize:
    """Test sliding window behavior."""
    
    def test_window_size_limit(self):
        """Test that measurements are limited by window size."""
        tracker = LatencyTracker(window_size=5)
        
        # Add 10 measurements
        for i in range(10):
            tracker.add_measurement("/api/v1/jobs", i, 200)
        
        # Should only have the last 5 measurements
        assert len(tracker.latencies["/api/v1/jobs"]) == 5
        assert tracker.request_counts["/api/v1/jobs"] == 10  # Count should not be limited
    
    def test_window_size_fifo(self):
        """Test that old measurements are removed (FIFO)."""
        tracker = LatencyTracker(window_size=3)
        
        tracker.add_measurement("/api/v1/jobs", 100, 200)
        tracker.add_measurement("/api/v1/jobs", 200, 200)
        tracker.add_measurement("/api/v1/jobs", 300, 200)
        tracker.add_measurement("/api/v1/jobs", 400, 200)  # Should remove 100
        
        latencies = list(tracker.latencies["/api/v1/jobs"])
        assert len(latencies) == 3
        assert 100 not in latencies
        assert 200 in latencies
        assert 300 in latencies
        assert 400 in latencies


class TestSLABudgets:
    """Test SLA budget definitions."""
    
    def test_latency_budgets_defined(self):
        """Test that latency budgets are defined for key endpoints."""
        assert "/api/v1/auth/register" in LATENCY_BUDGETS
        assert "/api/v1/auth/login" in LATENCY_BUDGETS
        assert "/api/v1/jobs" in LATENCY_BUDGETS
    
    def test_latency_budget_structure(self):
        """Test that latency budgets have correct structure."""
        for endpoint, budget in LATENCY_BUDGETS.items():
            assert "p95" in budget
            assert "p99" in budget
            assert budget["p95"] > 0
            assert budget["p99"] > 0
            assert budget["p99"] >= budget["p95"]  # P99 should be >= P95
    
    def test_error_rate_budget_defined(self):
        """Test that error rate budget is defined."""
        assert ERROR_RATE_BUDGET > 0
        assert ERROR_RATE_BUDGET < 1  # Should be a reasonable percentage


class TestMultipleEndpoints:
    """Test tracking multiple endpoints simultaneously."""
    
    def test_separate_endpoint_tracking(self):
        """Test that endpoints are tracked separately."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100, 200)
        tracker.add_measurement("/api/v1/auth/login", 50, 200)
        
        jobs_metrics = tracker.get_metrics("/api/v1/jobs")
        auth_metrics = tracker.get_metrics("/api/v1/auth/login")
        
        assert jobs_metrics["request_count"] == 1
        assert auth_metrics["request_count"] == 1
        assert jobs_metrics["latency_p50_ms"] == 100
        assert auth_metrics["latency_p50_ms"] == 50
    
    def test_endpoint_isolation(self):
        """Test that errors on one endpoint don't affect another."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100, 200)
        tracker.add_measurement("/api/v1/auth/login", 50, 500)
        
        jobs_metrics = tracker.get_metrics("/api/v1/jobs")
        auth_metrics = tracker.get_metrics("/api/v1/auth/login")
        
        assert jobs_metrics["error_rate"] == 0.0
        assert auth_metrics["error_rate"] == 1.0


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_single_measurement(self):
        """Test metrics with only one measurement."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 150, 200)
        
        metrics = tracker.get_metrics("/api/v1/jobs")
        assert metrics["latency_p50_ms"] == 150
        assert metrics["latency_p95_ms"] == 150
        assert metrics["latency_p99_ms"] == 150
    
    def test_all_errors(self):
        """Test endpoint with 100% error rate."""
        tracker = LatencyTracker(window_size=100)
        
        tracker.add_measurement("/api/v1/jobs", 100, 500)
        tracker.add_measurement("/api/v1/jobs", 150, 404)
        tracker.add_measurement("/api/v1/jobs", 200, 503)
        
        metrics = tracker.get_metrics("/api/v1/jobs")
        assert metrics["error_rate"] == 1.0
        assert metrics["error_count"] == 3
    
    def test_nonexistent_endpoint(self):
        """Test getting metrics for an endpoint with no data."""
        tracker = LatencyTracker(window_size=100)
        
        metrics = tracker.get_metrics("/api/v1/nonexistent")
        assert metrics["request_count"] == 0
        assert metrics["error_count"] == 0
        assert metrics["error_rate"] == 0.0
