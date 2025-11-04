# Story: Latency and Error Budgets

ID: ST-013  
Epic: Observability & Metrics  
Owner: TBD  
Status: drafted

## Description
Define latency and error budgets for key endpoints and add monitoring to ensure P95 targets and error rates stay within SLAs.

## Acceptance Criteria
1. Given API requests, then P95 latency is measured and reported for auth, jobs list, recommendations (when added), and apply.
2. Given failures, then error rates are tracked and alert thresholds documented.
3. Given regressions beyond budgets, then issues are visible on the dashboard or logs for action.

## Technical Notes
- Middleware timing; simple counters for status_code buckets

## Dependencies
- ST-011 Event Schema & Logging

## Tasks
- [ ] Define budgets per endpoint
- [ ] Add timers/counters
- [ ] Reporting

## FR Coverage
- FR-009 Metrics and logging

