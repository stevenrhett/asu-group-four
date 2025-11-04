# Story: Interview Scheduling - ICS + Email

ID: ST-009  
Epic: Employer Smart Inbox & Scheduling  
Owner: TBD  
Status: drafted

## Description
Generate calendar invites (ICS) and send email notifications for interview scheduling, including basic reschedule/cancel flows.

## Acceptance Criteria
1. Given a shortlisted candidate, when scheduling an interview, then an ICS file is generated with title, time, location/link, and attendees.
2. Given scheduling, then an email is sent to candidate and employer with ICS attached.
3. Given a reschedule/cancel, then updated ICS is generated and follow-up email is sent.

## Technical Notes
- ICS generation helper; provider-agnostic email abstraction (e.g., SendGrid-compatible)
- Store minimal audit log of scheduling actions

## Dependencies
- ST-006 Employer Smart Inbox - Basics

## Tasks
- [ ] ICS generation utility
- [ ] Email template + send API
- [ ] Backend route for scheduling (create/update/cancel)
- [ ] Tests

## FR Coverage
- FR-007 Interview scheduling basics
- FR-008 Notifications (scheduling emails)
