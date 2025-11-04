# Story: Status Change Emails

ID: ST-008  
Epic: Notifications  
Owner: TBD  
Status: in-review

## Description
Send email notifications to seekers and employers when an application status changes (applied, viewed, shortlisted, interview, rejected).

## Acceptance Criteria
1. Given a status update to any of the supported states, then an email is sent to the seeker with the new status and next steps.
2. Given a shortlist or interview state, then an email is sent to the employer confirming the action.
3. Given provider errors, then failures are logged and retried per policy; user-facing flows remain stable.

## Technical Notes
- Provider-agnostic abstraction (e.g., SendGrid-style API)
- Templated messages per status with placeholders

## Dependencies
- ST-014 Apply & Status Tracking

## Tasks
- [x] Email templates per status
- [x] Send utility with provider abstraction
- [x] Hook into status update path
- [x] Tests

## FR Coverage
- FR-008 Notifications (status changes)
