# Epics Overview

This document aggregates epics and links to detailed files, with story coverage and FR mapping.

## Epics

1) Onboarding & Profile — docs/epic-onboarding-profile.md  
   Stories:
   - ST-002 Resume Upload & Parsing — covers FR-002
   - ST-007 Seeker Minimal Profile Completion — supports FR-002 (profile readiness)
   - ST-008 Seeker Dashboard — supports FR-005 (status visibility)

2) Recommendations v1 — docs/epic-recommendations-v1.md  
   Stories:
   - ST-003 Job Index & Embeddings — covers FR-004
   - ST-004 Hybrid Scoring & Ranking — covers FR-004
   - ST-005 Explainability (Why this job?) — covers FR-004
   - ST-006 Feedback Capture & Logging — covers FR-004, FR-009

3) Employer Smart Inbox & Scheduling — docs/epic-employer-inbox-scheduling.md  
   Stories:
    - ST-006 Employer Smart Inbox Basics — covers FR-006
    - ST-009 Scheduling ICS + Email — covers FR-007, FR-008
    - ST-010 Candidate View & Shortlist Flow — covers FR-006
    - ST-015 Job Posting Management — covers FR-003

4) Authentication & Roles — docs/epic-auth.md  
   Stories:
   - ST-001 Auth & JWT — covers FR-001
   - ST-001a Role-Aware Navigation — supports FR-001

5) Notifications — docs/epic-notifications.md  
   Stories:
   - ST-008 Status Change Emails — covers FR-008
   - ST-009a Scheduling Email Template — covers FR-008

6) Observability & Metrics — docs/epic-observability.md  
   Stories:
   - ST-011 Event Schema & Logging — covers FR-009
   - ST-012 Metrics Dashboard (MVP) — covers FR-009
   - ST-013 Latency/Error Budgets — covers FR-009

---

Traceability: All MVP FRs (FR-001..FR-009) have story coverage across the above epics.
