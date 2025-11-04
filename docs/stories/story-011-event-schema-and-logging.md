# Story: Event Schema & Logging

ID: ST-011  
Epic: Observability & Metrics  
Owner: TBD  
Status: drafted

## Description
Define an event schema and implement structured logging for key funnels: recommendation views/clicks, applies, inbox actions, status changes, feedback.

## Acceptance Criteria
1. Given user actions on recommendations (view/click), then events are logged with anonymized user id, job id, timestamp, and context.
2. Given apply or status changes, then events are logged consistently with schema and retrievable for dashboards.
3. Given errors, then logs include correlation id and stack trace (non-sensitive) for debugging.

## Technical Notes
- JSON structured logs; include event_type, actor_id, subject_id, ts
- Consider a lightweight in-app events collection initially

## Dependencies
- ST-001 Auth (for user id)

## Tasks
- [ ] Event schema definition
- [ ] Logging helpers and middleware
- [ ] Instrument key flows
- [ ] Tests

## FR Coverage
- FR-009 Metrics and logging

