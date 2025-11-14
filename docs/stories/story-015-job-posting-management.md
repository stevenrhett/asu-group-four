# Story: Job Posting Management

ID: ST-015  
Epic: Employer Smart Inbox & Scheduling  
Owner: TBD  
Status: drafted

## Description
Allow employers to create, edit, and archive job postings with title, description, location, and skills.

## Acceptance Criteria
1. Given an employer, when creating a job, then required fields are validated and a job record is persisted.
2. Given an existing job, when edited, then changes are saved and visible in listings.
3. Given an existing job, when archived, then it no longer appears in active listings.

## Technical Notes
- FastAPI endpoints: POST/PUT/PATCH for jobs; archive flag
- Model: title, description, location, skills, status (active/archived)

## Dependencies
- ST-001 Auth & JWT (employer role)

## Tasks
- [ ] Job create/edit/archive endpoints
- [ ] Validation and model updates
- [ ] Tests

## FR Coverage
- FR-003 Job posting management

