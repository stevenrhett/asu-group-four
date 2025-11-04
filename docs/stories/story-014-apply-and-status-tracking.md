# Story: Apply Flow & Status Tracking

ID: ST-014  
Epic: Employer Smart Inbox & Scheduling  
Owner: TBD  
Status: drafted

## Description
Implement one-click apply for seekers and a status lifecycle (applied, viewed, shortlisted, interview, rejected) visible to both parties.

## Acceptance Criteria
1. Given a recommended job, when the seeker clicks apply, then an application record is created and seeker sees "applied" status.
2. Given employer actions (view/shortlist/interview/reject), then the application status updates and seeker is notified.
3. Given status changes, then updates are audit-logged and visible in both dashboards.

## Technical Notes
- Application model with status enum and timestamps
- Backend endpoints to update status; idempotent operations
- UI badges and filters; notifications via email

## Dependencies
- ST-001 Auth & JWT
- ST-006 Employer Smart Inbox - Basics

## Tasks
- [ ] Application model + CRUD endpoints
- [ ] Apply button + confirmation UI
- [ ] Status update endpoints and UI badges
- [ ] Notification hooks on status changes
- [ ] Tests

## FR Coverage
- FR-005 Application flow (apply & status)
- FR-008 Notifications (status changes)
