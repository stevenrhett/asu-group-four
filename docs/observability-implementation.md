# Observability & Metrics

**Status**: ✅ Implemented  
**Date Updated**: November 5, 2025  
**Stories**: ST-011 (Event Schema & Logging), ST-012 (Metrics Dashboard MVP)

This document describes the event logging and metrics system implemented for observability and monitoring.

## Implementation Summary

### Completed Components
- ✅ Event schema definitions with Pydantic V2
- ✅ Structured logging service
- ✅ Correlation ID middleware
- ✅ Metrics calculation service
- ✅ Metrics API endpoints
- ✅ Simple dashboard HTML
- ✅ Comprehensive test suite (26 tests passing)

### Files Created
- `backend/app/schemas/events.py` - Event schemas
- `backend/app/services/logging.py` - Logging service
- `backend/app/services/metrics.py` - Metrics service
- `backend/app/middleware/correlation.py` - Request correlation
- `backend/app/api/v1/routes/metrics.py` - API endpoints
- `backend/app/static/dashboard.html` - Dashboard UI
- `backend/tests/test_event_logging.py` - Event tests
- `backend/tests/test_metrics.py` - Metrics tests

## Overview

The observability system consists of:

1. **Event Schema & Logging (ST-011)**: Structured event logging with correlation IDs
2. **Metrics Dashboard (ST-012)**: KPI tracking and visualization

## Event Schema

### Event Types

All events in the system follow a standardized schema defined in `app/schemas/events.py`:

- **Recommendation Events**: `recommendation.view`, `recommendation.click`
- **Application Events**: `application.submitted`, `application.status_changed`
- **Inbox Events**: `inbox.candidate_viewed`, `inbox.candidate_shortlisted`, `inbox.candidate_rejected`
- **Feedback Events**: `feedback.submitted`
- **Resume Events**: `resume.uploaded`, `resume.parsed`
- **Job Events**: `job.posted`, `job.indexed`
- **Error Events**: `error.occurred`
- **System Events**: `system.startup`, `system.shutdown`

### Event Fields

All events include:
- `event_type`: Type of event (from EventType enum)
- `timestamp`: ISO 8601 timestamp
- `correlation_id`: Request correlation ID for tracing
- `actor_id`: User ID who triggered the event
- `severity`: Event severity (debug, info, warning, error, critical)
- `metadata`: Additional event-specific data

## Structured Logging

### Using the Logger

```python
from app.services.logging import logger

# Log a recommendation view
logger.log_recommendation_view(
    job_id="job_123",
    candidate_id="user_456",
    score=0.85,
    rank=1,
    context="homepage"
)

# Log an application submission
logger.log_application_submitted(
    application_id="app_789",
    job_id="job_123",
    candidate_id="user_456"
)

# Log an error
logger.log_error(
    error_type="ValueError",
    error_message="Invalid input",
    stack_trace=traceback_string,
    request_path="/api/v1/jobs",
    request_method="POST",
    user_id="user_456"
)
```

### Correlation IDs

Correlation IDs are automatically managed by middleware and track requests across services:

```python
from app.services.logging import set_correlation_id, get_correlation_id

# Set correlation ID (usually done by middleware)
correlation_id = set_correlation_id()

# Get current correlation ID
current_id = get_correlation_id()
```

## Middleware

### LoggingMiddleware

Automatically tracks all HTTP requests with:
- Request method and path
- Response status code
- Request duration
- Correlation ID
- Error logging with stack traces

```python
# Added to main.py
from app.core.middleware import LoggingMiddleware

app.add_middleware(LoggingMiddleware)
```

### MetricsMiddleware

Tracks performance metrics:
- Request count
- Error count
- Response times

## Metrics & KPIs

### Available Metrics

The metrics service tracks:

1. **Click-Through Rate (CTR)**: Recommendation views vs clicks
2. **Conversion Rate**: Applications per recommendation click
3. **Time-to-Shortlist**: Median time from application to shortlist
4. **Engagement**: Total events and unique users

### API Endpoints

#### Get KPIs

```http
GET /api/v1/metrics/kpis
```

Query parameters:
- `start_date` (optional): ISO 8601 datetime
- `end_date` (optional): ISO 8601 datetime

Response:
```json
{
  "success": true,
  "data": {
    "period_start": "2025-10-01T00:00:00",
    "period_end": "2025-11-01T00:00:00",
    "recommendation_views": 1000,
    "recommendation_clicks": 300,
    "ctr": 0.3,
    "applications_submitted": 150,
    "application_conversion_rate": 0.5,
    "candidates_shortlisted": 75,
    "median_time_to_shortlist": 3600.0,
    "total_events": 2000,
    "unique_users": 250
  }
}
```

#### Get CTR Time Series

```http
GET /api/v1/metrics/ctr/timeseries
```

Query parameters:
- `start_date` (optional): ISO 8601 datetime
- `end_date` (optional): ISO 8601 datetime
- `bucket_hours` (default: 24): Time bucket size in hours (1-168)

Response:
```json
{
  "success": true,
  "data": [
    {
      "timestamp": "2025-10-01T00:00:00",
      "value": 0.28,
      "label": "CTR"
    },
    {
      "timestamp": "2025-10-02T00:00:00",
      "value": 0.32,
      "label": "CTR"
    }
  ]
}
```

#### Get Conversion Time Series

```http
GET /api/v1/metrics/conversion/timeseries
```

Same query parameters as CTR time series.

### Metrics Dashboard

A simple HTML dashboard is available at:

```
/app/static/dashboard.html
```

The dashboard provides:
- Real-time KPI cards
- CTR trend chart
- Conversion rate trend chart
- Configurable time periods
- Auto-refresh every 5 minutes

To serve the dashboard, configure FastAPI to serve static files:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

Then access at: `http://localhost:8000/static/dashboard.html`

## Integration Examples

### Logging Recommendation Views

In `app/api/v1/routes/recommendations.py`:

```python
from app.services.logging import logger

@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(...):
    # ... existing code ...
    
    # Log recommendation views
    for rank, rec in enumerate(results, 1):
        logger.log_recommendation_view(
            job_id=str(rec.job_id),
            candidate_id=str(current_user.id),
            score=rec.score,
            rank=rank,
            context="api"
        )
    
    return RecommendationResponse(results=results)
```

### Logging Application Submissions

In `app/api/v1/routes/applications.py`:

```python
from app.services.logging import logger

@router.post("/")
async def submit_application(...):
    # ... create application ...
    
    logger.log_application_submitted(
        application_id=str(application.id),
        job_id=str(application.job_id),
        candidate_id=str(current_user.id)
    )
    
    return application
```

### Logging Inbox Actions

In `app/api/v1/routes/inbox.py`:

```python
from app.services.logging import logger
from datetime import datetime

@router.patch("/{application_id}/status")
async def update_status(...):
    # ... update status ...
    
    # Calculate time since application
    time_since = (datetime.utcnow() - application.created_at).total_seconds()
    
    logger.log_inbox_action(
        employer_id=str(current_user.id),
        candidate_id=str(application.candidate_id),
        job_id=str(application.job_id),
        action=new_status,  # "viewed", "shortlisted", "rejected"
        time_since_application=time_since
    )
    
    return application
```

## Testing

Run tests for the observability features:

```bash
pytest tests/test_event_logging.py -v
pytest tests/test_metrics.py -v
```

## Production Considerations

### Event Storage

The MVP implementation uses an in-memory event store. For production:

1. **Time-Series Database**: Use InfluxDB, TimescaleDB, or Prometheus
2. **Log Aggregation**: Use ELK Stack (Elasticsearch, Logstash, Kibana) or similar
3. **Cloud Services**: Use AWS CloudWatch, Google Cloud Logging, or Azure Monitor

### Metrics Export

Consider exporting metrics to:
- **Prometheus**: For alerting and monitoring
- **Grafana**: For advanced visualization
- **Datadog/New Relic**: For APM and distributed tracing

### Privacy & Compliance

- Anonymize user IDs where required
- Implement data retention policies
- Filter sensitive data from logs
- Add audit logging for compliance

## Configuration

Environment variables for observability:

```env
# Logging level
LOG_LEVEL=INFO

# Metrics retention period (days)
METRICS_RETENTION_DAYS=90

# Enable/disable specific event types
ENABLE_RECOMMENDATION_LOGGING=true
ENABLE_APPLICATION_LOGGING=true
ENABLE_ERROR_LOGGING=true
```

## Troubleshooting

### Events not appearing

1. Check that middleware is enabled in `main.py`
2. Verify logger is imported: `from app.services.logging import logger`
3. Check correlation ID is set: `get_correlation_id()`

### Metrics not calculating

1. Ensure events are being added to metrics service
2. Check date range filters
3. Verify event types match expected values

### Dashboard not loading

1. Check API endpoints are accessible
2. Verify CORS settings allow dashboard origin
3. Check browser console for errors
4. Ensure authentication is configured correctly

## Future Enhancements

- [ ] Real-time event streaming
- [ ] Alerting on anomalies
- [ ] User journey tracking
- [ ] A/B testing support
- [ ] Custom dashboards per employer
- [ ] Export reports to CSV/PDF
- [ ] Integration with BI tools
