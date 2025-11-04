# Job Portal - Product Requirements Document (PRD)

**Author:** Team 4  
**Date:** 2025-11-04  
**Version:** 1.0

---

## Executive Summary
A two-sided job marketplace connecting job seekers and employers with explainable, AI-driven matching. The MVP delivers a thin, end-to-end slice: Auth → Profile/Resume Parse → Recommend → Apply → Status → Email. Emphasis on transparency ("Why this job?"), speed to value, and measurable outcomes.

### What Makes This Special
- Explainable recommendations that build trust for both sides
- Employer smart inbox to reduce time-to-shortlist
- Feedback loops to continuously improve relevance

---

## Project Classification
**Technical Type:** Web application (Next.js + FastAPI)  
**Domain:** HR Tech / Job Marketplace  
**Complexity:** Level 3 (PRD + Architecture)

---

## Success Criteria
- +20–30% CTR on recommended jobs within 2 weeks of pilot
- +15% apply-start rate from recommendations
- >70% perceived relevance in user feedback prompts
- Employer: time-to-shortlist under 2 days for pilot roles

### Business Metrics
- Seeker conversion: profile completion → first apply
- Employer conversion: post → shortlist → interview scheduled
- Engagement: DAU/WAU ratio, notification CTR, repeat applications

---

## Product Scope

### MVP - Minimum Viable Product
- Auth (JWT), role-aware (seeker/employer)
- Job seeker onboarding with resume upload + parsing
- Job recommendations v1 (BM25 + embeddings + explainability)
- One-click apply and application status tracking
- Employer posting + smart inbox (filters, shortlist)
- Basic interview scheduling (ICS export) and notification emails

### Growth Features (Post-MVP)
- Skills graph/ontology; learn-to-rank reranker
- Calendar provider integration; ATS import/export
- Fairness auditing + relevance dashboards
- Candidate summaries and interview-question suggestions

### Vision (Future)
- Career copilot; real-time market intelligence; AI recruiter sidekick

---

## Domain-Specific Requirements
- Transparency in recommendations (top skills/terms contributing)
- Anti-abuse controls (spam prevention, duplicate job checks)
- Privacy-first handling of resumes and PII

---

## User Experience Principles
- Clarity over cleverness; explainability as default
- Minimize first-session friction; show value in minutes
- Reduce anxiety: visible status and feedback channels

### Key Interactions
- Seeker: upload resume → see recommendations → apply → track status
- Employer: post job → triage inbox → shortlist → schedule

---

## Functional Requirements
FR-001 Authentication and Authorization (JWT, password hashing, role claim)
FR-002 Resume upload and parsing to extract skills, titles, experience
FR-003 Job posting management (create, edit, archive)
FR-004 Recommendation engine v1 (hybrid retrieval with explainability)
FR-005 Application flow: apply, track, update statuses
FR-006 Employer smart inbox (filters, shortlist, candidate view)
FR-007 Interview scheduling basics (ICS file generation)
FR-008 Email notifications for key events (apply, status change, scheduling)
FR-009 Metrics and logging (clicks, applies, inbox actions)

---

## Non-Functional Requirements
### Performance
- P95 recommendation generation under 400ms per request (excluding embedding index build)

### Security
- Strong password hashing (bcrypt), JWT with rotation, input validation

### Scalability
- Indexing pipeline for jobs and resumes; horizontal-ready API

### Accessibility
- WCAG 2.1 AA for primary flows

### Integration
- ChromaDB for embeddings; email provider (e.g., SendGrid compatible abstraction)

---

## Project-Type Specific Requirements

### API Specification (Initial)
- Auth
  - POST /api/v1/auth/register — create user (seeker/employer)
  - POST /api/v1/auth/login — issue JWT (includes role claim)
- Jobs
  - GET /api/v1/jobs — list jobs
  - POST /api/v1/jobs — create job posting
- Applications
  - POST /api/v1/applications — create application (apply)
  - GET /api/v1/applications — list applications
  - PATCH /api/v1/applications/{id}/status — update status (applied/viewed/shortlisted/interview/rejected)
- Scheduling
  - POST /api/v1/scheduling — create interview (returns ICS)
  - PUT /api/v1/scheduling/{id} — reschedule (returns ICS)
  - DELETE /api/v1/scheduling/{id} — cancel

### Authentication & Authorization
- JWT access tokens signed with HS256; includes `sub` (user id) and `role` (`seeker` or `employer`).
- Protected routes require bearer token; role-based checks on employer-only endpoints.

---

## Implementation Planning
### Epics (initial)
- Onboarding & Profile (resume parsing)
- Recommendations v1 (hybrid + explainability + feedback)
- Employer Smart Inbox & Scheduling
- Authentication & Roles
- Notifications
- Observability & Metrics

Next: create epics and seed first sprint stories.

---

## References
- Context: docs/Job Portal.md  
- Brainstorming: docs/brainstorming-session-results-2025-11-04.md  
- Design Thinking: docs/design-thinking-2025-11-04.md  
- Problem Solving: docs/problem-solution-2025-11-04.md  
- Storytelling: docs/story-2025-11-04.md
