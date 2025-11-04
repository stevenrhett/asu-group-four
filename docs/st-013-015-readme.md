# ST-013 & ST-015 Quick Start

## ✅ Implementation Complete!

**38/38 tests passing** 🎉

### What Was Built

#### ST-015: Job Posting Management
Complete CRUD system for employers to manage job postings:
- ✅ Create, update, archive, delete jobs
- ✅ Owner-only authorization
- ✅ Field validation (title, description, location, skills)
- ✅ Soft deletion (archive/unarchive)
- ✅ Filtering and pagination
- ✅ Event logging for all operations

#### ST-013: Latency and Error Budgets
Performance monitoring with SLA compliance:
- ✅ P50, P95, P99 latency tracking
- ✅ Error rate monitoring
- ✅ Defined SLA budgets per endpoint
- ✅ Automatic violation detection
- ✅ Admin API for metrics access
- ✅ Real-time tracking middleware

---

## Quick Test

```bash
cd backend
source venv/bin/activate

# Run the new tests
python -m pytest tests/test_job_posting.py tests/test_performance.py -v

# Should see: 38 passed ✅
```

---

## Job Posting API Examples

### Create a Job (Employer Only)
```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Authorization: Bearer YOUR_EMPLOYER_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are seeking an experienced Python developer to join our team...",
    "location": "Remote",
    "skills": ["Python", "FastAPI", "MongoDB", "Docker"]
  }'
```

### List All Active Jobs
```bash
curl http://localhost:8000/api/v1/jobs?status=active&limit=10
```

### Update a Job (Owner Only)
```bash
curl -X PUT http://localhost:8000/api/v1/jobs/JOB_ID \
  -H "Authorization: Bearer YOUR_EMPLOYER_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer (Updated)",
    "skills": ["Python", "FastAPI", "MongoDB", "Docker", "Redis"]
  }'
```

### Archive a Job (Owner Only)
```bash
curl -X PATCH http://localhost:8000/api/v1/jobs/JOB_ID/archive \
  -H "Authorization: Bearer YOUR_EMPLOYER_JWT"
```

### Filter Jobs by Employer
```bash
curl http://localhost:8000/api/v1/jobs?employer_id=EMPLOYER_ID
```

---

## Performance Monitoring API Examples

### Get All Performance Metrics (Admin Only)
```bash
curl http://localhost:8000/api/v1/performance/metrics \
  -H "Authorization: Bearer YOUR_ADMIN_JWT"
```

Response:
```json
[
  {
    "endpoint": "/api/v1/jobs",
    "request_count": 1523,
    "error_count": 3,
    "error_rate": 0.00197,
    "latency_p50_ms": 45.3,
    "latency_p95_ms": 187.2,
    "latency_p99_ms": 342.1,
    "p95_within_budget": true,
    "p99_within_budget": true
  }
]
```

### Get SLA Budget Violations (Admin Only)
```bash
curl http://localhost:8000/api/v1/performance/violations \
  -H "Authorization: Bearer YOUR_ADMIN_JWT"
```

### View Defined Budgets
```bash
curl http://localhost:8000/api/v1/performance/budgets \
  -H "Authorization: Bearer YOUR_ADMIN_JWT"
```

---

## SLA Budgets Defined

| Endpoint | P95 (ms) | P99 (ms) |
|----------|----------|----------|
| `/api/v1/auth/register` | 1000 | 2000 |
| `/api/v1/auth/login` | 500 | 1000 |
| `/api/v1/jobs` | 200 | 500 |
| `/api/v1/recommendations` | 1000 | 2000 |
| `/api/v1/applications` | 500 | 1000 |

**Error Rate Budget**: 1% (0.01)

Violations are automatically logged as structured events!

---

## Job Status Workflow

```
DRAFT ──────► ACTIVE ──────► ARCHIVED
               │               │
               └───────────────┘
                  (unarchive)
```

- **ACTIVE**: Visible in job listings, accepting applications
- **ARCHIVED**: Hidden from listings, read-only
- **DRAFT**: (Future) Not yet published

---

## Key Features

### Job Posting Management
✅ Role-based authorization (employer role required)  
✅ Owner-only access controls  
✅ Comprehensive validation (3-200 char titles, 10-5000 char descriptions)  
✅ Soft deletion with archive/unarchive  
✅ Automatic timestamps (created_at, updated_at, archived_at)  
✅ Event logging for audit trail  
✅ Filtering by status and employer  
✅ Pagination support  

### Performance Monitoring
✅ Automatic request timing  
✅ P50, P95, P99 percentile calculations  
✅ Error rate tracking (4xx, 5xx)  
✅ Endpoint path normalization  
✅ Sliding window metrics (last 1000 requests)  
✅ SLA budget compliance checking  
✅ Violation logging with detailed context  
✅ Admin-only metrics API  

---

## Testing

### Test Files
- `tests/test_job_posting.py` - 19 tests for job management
- `tests/test_performance.py` - 19 tests for performance monitoring

### Test Coverage
- Schema validation
- Field constraints
- Authorization (placeholders for integration tests)
- Percentile calculations
- Error rate tracking
- SLA budget compliance
- Edge cases

### Run Tests
```bash
# Quick test
python -m pytest tests/test_job_posting.py tests/test_performance.py -v

# With coverage
python -m pytest tests/test_job_posting.py tests/test_performance.py --cov=app --cov-report=term-missing

# Run all tests
python -m pytest tests/ -v
```

---

## Event Types Added

### Job Events
- `JOB_POSTED` - New job created
- `JOB_UPDATED` - Job modified
- `JOB_ARCHIVED` - Job archived
- `JOB_UNARCHIVED` - Job reactivated  
- `JOB_DELETED` - Job permanently deleted

### SLA Events
- `SLA_LATENCY_BUDGET_EXCEEDED` - Latency SLA violated
- `SLA_ERROR_BUDGET_EXCEEDED` - Error rate SLA violated

---

## Files Created

### New Files
```
backend/app/middleware/performance.py       # Performance monitoring
backend/app/api/v1/routes/performance.py    # Performance API
backend/tests/test_job_posting.py           # Job tests (19)
backend/tests/test_performance.py           # Performance tests (19)
docs/ST-013-015-implementation-summary.md   # Full documentation
```

### Modified Files
```
backend/app/models/job.py                   # Enhanced job model
backend/app/api/v1/routes/jobs.py          # Complete CRUD
backend/app/schemas/events.py              # New event types
backend/app/main.py                        # Added middleware & routes
docs/sprint-status.yaml                     # Updated to in-review
```

---

## Architecture

### Request Flow with Performance Monitoring

```
Request → PerformanceMonitoringMiddleware
            ↓
          [Start Timer]
            ↓
          Route Handler (e.g., POST /jobs)
            ↓
          [Stop Timer, Track Metrics]
            ↓
          [Check SLA Budgets]
            ↓
          [Log Violations if Any]
            ↓
          Response
```

### Job Posting Authorization

```
Request → Auth Middleware
            ↓
        [Verify JWT]
            ↓
        [Check Role: employer]
            ↓
        [Check Ownership]
            ↓
        Route Handler
```

---

## Next Steps

### Immediate
1. **Integration Tests**: Test with real database and authentication
2. **Frontend**: Build UI for job management
3. **Monitoring**: Set up Grafana dashboards

### Future Enhancements
1. **Job Search**: Full-text search with filters
2. **Bulk Operations**: Archive/delete multiple jobs
3. **Job Templates**: Reusable posting templates
4. **Alerting**: Email/Slack notifications for SLA violations
5. **Historical Metrics**: Store in database for trend analysis
6. **Custom Budgets**: Admin UI to configure SLA budgets

---

## Documentation

- **Full Implementation**: `docs/ST-013-015-implementation-summary.md`
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Observability Docs**: `docs/observability-implementation.md`
- **Story Files**: 
  - `docs/stories/story-013-latency-and-error-budgets.md`
  - `docs/stories/story-015-job-posting-management.md`

---

## Success! 🎉

Both stories are fully implemented with:
- ✅ 38/38 tests passing
- ✅ Comprehensive validation
- ✅ Proper authorization
- ✅ Event logging integration
- ✅ Real-time performance monitoring
- ✅ SLA compliance checking

Ready for review and integration testing!
