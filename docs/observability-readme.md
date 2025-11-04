# Observability Quick Start

## ST-011 & ST-012 Implementation Complete! 🎉

All 26 tests passing ✅

## What Was Built

### Event Logging (ST-011)
- **Structured logging** with standardized event schemas
- **Correlation ID tracking** across all requests
- **Event types** for recommendations, applications, inbox actions, and errors
- **JSON output** for easy integration with log aggregation tools

### Metrics Dashboard (ST-012)
- **KPI tracking**: CTR, conversion rates, time-to-action metrics
- **Time-series data**: Track metrics over time with configurable granularity
- **API endpoints**: REST API for programmatic access
- **Simple dashboard**: HTML dashboard for visualization

## Quick Start

### 1. Set Up Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install 'pydantic[email]'  # Required for email validation
```

### 2. Run Tests

```bash
# Run all observability tests
python -m pytest tests/test_event_logging.py tests/test_metrics.py -v

# Run with coverage
python -m pytest tests/test_event_logging.py tests/test_metrics.py --cov=app/services --cov=app/schemas
```

### 3. Use Event Logging

```python
from app.services.logging import event_logger

# Log a recommendation view
event_logger.log_recommendation_view(
    user_id="user123",
    job_id="job456",
    position=1,
    algorithm="hybrid",
    score=0.85
)

# Log an application submission
event_logger.log_application_submitted(
    user_id="user123",
    job_id="job456",
    application_id="app789"
)

# Log an error
event_logger.log_error(
    error_type="ValidationError",
    message="Invalid resume format",
    user_id="user123"
)
```

### 4. Access Metrics

```python
from app.services.metrics import metrics_service
from datetime import datetime, timedelta

# Add events to metrics
metrics_service.add_event(event)

# Get KPIs
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=7)
kpis = metrics_service.get_kpis(start_date, end_date)

print(f"CTR: {kpis.recommendation.ctr:.2%}")
print(f"Conversion: {kpis.recommendation.conversion_rate:.2%}")
```

### 5. Use the API

Start the server:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Access endpoints:
- **Dashboard**: http://localhost:8000/metrics/dashboard
- **KPIs**: http://localhost:8000/api/v1/metrics/kpis
- **Time-series**: http://localhost:8000/api/v1/metrics/time-series/ctr?start_date=2025-11-01T00:00:00&end_date=2025-11-05T23:59:59

## Key Features

### Correlation ID Middleware
Every request automatically gets a correlation ID for distributed tracing:

```python
from app.middleware.correlation import get_correlation_id

# In any request handler
correlation_id = get_correlation_id()
```

### Pydantic V2 Compatible
All schemas use modern Pydantic V2 with `ConfigDict`:

```python
class BaseEvent(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
```

### Extensible Metadata
All events support custom metadata:

```python
event_logger.log_recommendation_view(
    user_id="user123",
    job_id="job456",
    metadata={
        "source": "homepage",
        "device": "mobile",
        "experiment_group": "A"
    }
)
```

## Testing

All test categories covered:
- ✅ Event schema validation
- ✅ Logging operations
- ✅ Correlation ID tracking
- ✅ Metrics calculation (CTR, conversion, etc.)
- ✅ Time period filtering
- ✅ Time-series generation

## Next Steps

1. **Database Integration**: Persist events to MongoDB
2. **Real-time Updates**: WebSocket support for live dashboards
3. **Alerting**: Set up threshold-based alerts
4. **Export**: CSV/JSON export functionality
5. **Advanced Visualizations**: Charts and graphs

## Documentation

- Full implementation details: `docs/observability-implementation.md`
- API documentation: http://localhost:8000/docs (when server is running)
- Event schemas: `backend/app/schemas/events.py`
- Test examples: `backend/tests/test_event_logging.py` and `backend/tests/test_metrics.py`

## Troubleshooting

### Virtual Environment Issues
If the Python environment configuration gets stuck:
```bash
# Manually create venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install 'pydantic[email]'
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
pip install 'pydantic[email]'
```

### Test Failures
Run with verbose output:
```bash
python -m pytest tests/test_event_logging.py tests/test_metrics.py -v -s
```

## Contact

For questions about the observability implementation, see:
- Story files: `docs/stories/story-011-event-schema-and-logging.md` and `story-012-metrics-dashboard-mvp.md`
- Implementation doc: `docs/observability-implementation.md`
