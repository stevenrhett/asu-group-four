# Story: Employer Smart Inbox - Basics

ID: ST-006  
Epic: Employer Smart Inbox & Scheduling  
Owner: TBD  
Status: drafted

## Description
Create core inbox with filters (new, viewed, shortlisted, interview, rejected) and item list view.

## Acceptance Criteria
1. Given applications, when loading inbox, then filter tabs show counts and filter the list.
2. Given an item, when clicked, then candidate detail opens with core signals.
3. Given shortlist action, then status updates and counts reflect immediately.

## Technical Notes
- Next.js App Router; FastAPI endpoints; optimistic updates

## Dependencies
- ST-001 Auth & JWT

## Tasks
- [ ] Inbox UI + filters
- [ ] Backend endpoints for list/update
- [ ] Tests

## FR Coverage
- FR-006 Employer smart inbox
