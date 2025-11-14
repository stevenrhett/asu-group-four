"""
Metrics and dashboard API endpoints.

Provides access to KPIs and time-series data for monitoring
and observability dashboards.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel

from app.services.metrics import metrics_service, KPIMetrics, TimeSeriesMetric
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter(prefix="/metrics", tags=["metrics"])


class MetricsResponse(BaseModel):
    """Response model for metrics endpoints."""
    
    success: bool = True
    data: KPIMetrics


class TimeSeriesResponse(BaseModel):
    """Response model for time-series endpoints."""
    
    success: bool = True
    data: list[TimeSeriesMetric]


@router.get("/kpis", response_model=MetricsResponse)
async def get_kpis(
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    current_user: User = Depends(get_current_user),
):
    """
    Get key performance indicators.
    
    Returns aggregated metrics including:
    - Click-through rate (CTR)
    - Application conversion rate
    - Time-to-shortlist
    - Engagement metrics
    
    Requires authentication. Admin users see all metrics,
    employers see their own metrics.
    """
    # Calculate KPIs
    kpis = metrics_service.get_kpis(
        start_date=start_date,
        end_date=end_date,
    )
    
    return MetricsResponse(data=kpis)


@router.get("/ctr/timeseries", response_model=TimeSeriesResponse)
async def get_ctr_timeseries(
    start_date: Optional[datetime] = Query(None, description="Start date for time series"),
    end_date: Optional[datetime] = Query(None, description="End date for time series"),
    bucket_hours: int = Query(24, description="Time bucket size in hours", ge=1, le=168),
    current_user: User = Depends(get_current_user),
):
    """
    Get click-through rate over time.
    
    Returns time-series data showing CTR trends.
    Useful for identifying patterns and anomalies.
    """
    bucket_size = timedelta(hours=bucket_hours)
    
    time_series = metrics_service.get_ctr_time_series(
        start_date=start_date,
        end_date=end_date,
        bucket_size=bucket_size,
    )
    
    return TimeSeriesResponse(data=time_series)


@router.get("/conversion/timeseries", response_model=TimeSeriesResponse)
async def get_conversion_timeseries(
    start_date: Optional[datetime] = Query(None, description="Start date for time series"),
    end_date: Optional[datetime] = Query(None, description="End date for time series"),
    bucket_hours: int = Query(24, description="Time bucket size in hours", ge=1, le=168),
    current_user: User = Depends(get_current_user),
):
    """
    Get application conversion rate over time.
    
    Returns time-series data showing conversion trends.
    """
    bucket_size = timedelta(hours=bucket_hours)
    
    time_series = metrics_service.get_conversion_time_series(
        start_date=start_date,
        end_date=end_date,
        bucket_size=bucket_size,
    )
    
    return TimeSeriesResponse(data=time_series)


@router.get("/health")
async def metrics_health():
    """
    Health check for metrics service.
    
    Returns basic statistics about the metrics system.
    """
    total_events = len(metrics_service.event_store)
    
    return {
        "success": True,
        "service": "metrics",
        "status": "healthy",
        "total_events": total_events,
    }
