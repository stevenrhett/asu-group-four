# Sprint Plan — Sprint 1

generated: 2025-11-04
project: asu-group-four
current_sprint: "Sprint 1"

## Sprint Goal
Deliver a thin, end-to-end MVP slice: Auth → Resume Upload/Parsing → Recommend (hybrid + explainability) → Apply → Status visibility. A seeker can register, upload a resume to seed profile data, receive explainable recommendations, apply to a job, and see status updates.

## Scope (Stories)
- ST-001 Auth & JWT — docs/stories/story-001-auth-and-jwt.md
- ST-002 Resume Upload & Parsing — docs/stories/story-002-resume-upload-and-parsing.md
- ST-003 Job Index & Embeddings — docs/stories/story-003-job-index-and-embeddings.md
- ST-004 Hybrid Scoring & Ranking — docs/stories/story-004-hybrid-scoring-and-ranking.md
- ST-005 Explainability — docs/stories/story-005-explainability-why-this-job.md
- ST-014 Apply & Status Tracking — docs/stories/story-014-apply-and-status-tracking.md

Out of scope for Sprint 1: employer inbox UI basics, scheduling emails, extended dashboards.

## Deliverables
- Backend endpoints operational: auth, jobs, applications, scheduling (minimal), uploads (new), recommendations (new)
- Services: parsing_service, recommend_service, events (logging helper)
- Data models wired via Beanie: user, job, application, profile (new)
- Frontend: login flow, simple recommendations list with explanation chips, apply button with status badge
- E2E path verified locally: register → login → upload → recommend → apply → status

## Backlog Ordering (by value and dependency)
1) ST-001 Auth & JWT
2) ST-002 Resume Upload & Parsing
3) ST-003 Job Index & Embeddings
4) ST-004 Hybrid Scoring & Ranking
5) ST-005 Explainability
6) ST-014 Apply & Status Tracking

## Task Breakdown (by story)

ST-001 Auth & JWT (status: in-progress; size: M)
- Backend
  - Ensure JWT includes `role` claim; verify role checks on protected endpoints
  - Harden error responses; add basic tests for register/login
- Frontend
  - Create login page and store token; guard protected views
- Testing
  - FastAPI TestClient route tests for register/login

ST-002 Resume Upload & Parsing (status: ready-for-dev; size: M)
- Backend
  - Route `POST /api/v1/uploads/resume` (multipart)
  - `app/services/parsing_service.py` with simple text extract + skills keyword match
  - Persist parsed skills to `Profile` model (create `app/models/profile.py`)
- Frontend
  - Upload UI; display parsed skills preview
- Testing
  - Unit tests for parser fixtures; integration test for upload route

ST-003 Job Index & Embeddings (status: ready-for-dev; size: L)
- Backend
  - ChromaDB client init; env config for embeddings provider
  - Normalization tables for skills/titles; index builder in `recommend_service`
  - Batch embedding creation; persistence of job vectors
- Data
  - Seed script or fixtures for sample jobs
- Testing
  - Unit tests for normalization; smoke test for index/search

ST-004 Hybrid Scoring & Ranking (status: ready-for-dev; size: M)
- Backend
  - Weighted combiner (BM25 + cosine); config weights via env
  - Fallback to BM25 only if embeddings unavailable
- Testing
  - Unit tests for combiner behavior and fallback

ST-005 Explainability (status: ready-for-dev; size: S/M)
- Backend
  - Return top contributing skills/terms per result from scoring pipeline
- Frontend
  - Explanation chips component; expandable details
- Testing
  - Cases with/without explanation payload

ST-014 Apply & Status Tracking (status: ready-for-dev; size: M)
- Backend
  - Verify POST apply creates Application with user context
  - PATCH status endpoint correctness and audit logging (events helper)
- Frontend
  - Apply button on recommendation card; status badges list
- Testing
  - Integration tests for apply + status updates

## Milestones (target cadence)
- Day 1–2: ST-001 complete; scaffold uploads/recommendations routes
- Day 1–3: ST-002 backend + basic UI
- Day 2–5: ST-003 index build and search path
- Day 4–6: ST-004 scoring combiner finalized
- Day 6–7: ST-005 explanation end-to-end
- Day 6–8: ST-014 apply + status UI and backend polish
- Day 9: Hardening, E2E walkthrough, defect triage
- Day 10: Buffer, demo prep

## Risks & Mitigations
- Embeddings provider access or latency
  - Mitigation: allow local embedding fallback; cache vectors; tune batch sizes
- Resume parsing quality
  - Mitigation: keep heuristic parser simple, iterate post-sprint; allow manual edits in UI
- Data sparsity for recommendations
  - Mitigation: seed sample jobs; use BM25 fallback when vectors missing

## Definition of Ready (DoR)
- Story has clear acceptance criteria
- Dependencies identified; API paths drafted
- Test approach noted; data/fixtures available or planned

## Definition of Done (DoD)
- Acceptance criteria pass in local environment
- Unit/integration tests added and green
- API documented in README or route docstrings
- Demo script prepared for E2E scenario

## Ceremonies
- Daily standup (15 min): blockers, plan, progress
- Mid-sprint review/checkpoint: dependency/risk review
- Sprint review/demo: E2E walk-through of MVP slice
- Retrospective: what went well, what to improve

## Ownership & Handoffs
- Owners: TBD per story (assign at kickoff)
- Handoffs: backend to frontend when endpoints stable; provide Postman collection or curl examples

## References
- PRD — docs/PRD.md
- Architecture — docs/architecture.md
- Tech Spec — docs/tech-spec.md
- Sprint Status (tracking) — docs/sprint-status.yaml

