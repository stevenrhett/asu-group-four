## asu-group-four - Technical Specification

**Author:** Team 4  
**Date:** 2025-11-04  
**Project Level:** 3 (PRD + Architecture)  
**Change Type:** MVP Vertical Slice (Sprint 1)  
**Development Context:** Greenfield

---

## Context

### Available Documents
- PRD: docs/PRD.md
- Architecture: docs/architecture.md
- Epics: docs/epics.md
- Sprint Plan: docs/sprint-status.yaml (Sprint 1 approved)
- Stories (Sprint 1):
  - ST-001 Auth & JWT — docs/stories/story-001-auth-and-jwt.md
  - ST-002 Resume Upload & Parsing — docs/stories/story-002-resume-upload-and-parsing.md
  - ST-003 Job Index & Embeddings — docs/stories/story-003-job-index-and-embeddings.md
  - ST-004 Hybrid Scoring & Ranking — docs/stories/story-004-hybrid-scoring-and-ranking.md
  - ST-005 Explainability — docs/stories/story-005-explainability-why-this-job.md
  - ST-014 Apply & Status Tracking — docs/stories/story-014-apply-and-status-tracking.md

### Project Stack
- Frontend: Next.js 14.2.0 (App Router), React 18
- Backend: FastAPI, Uvicorn, Pydantic, Beanie (MongoDB), Motor
- Vector Store: ChromaDB; embeddings (OpenAI text-embedding-3-small or local)
- Auth: JWT (HS256) via python-jose; bcrypt via passlib
- Notifications: provider-agnostic (SendGrid-compatible abstraction)
- Scheduling: ICS (RFC 5545) minimal generator
- Runtime: Node 18+, Python 3.11+, MongoDB 6.x

### Existing Codebase Structure
- Backend: backend/app/api/v1/routes/{auth,jobs,applications,scheduling}.py; models {user,job,application}.py; core {config,security}.py; db/init_db.py
- Frontend: frontend/app/{layout.tsx,page.tsx}

---

## The Change

### Problem Statement
Deliver a thin, end-to-end MVP slice that lets a job seeker register/login, upload a resume to seed profile data, receive explainable recommendations, apply to jobs, and track application status. Employers post jobs and triage incoming applications (initial basics in Sprint 2).

### Proposed Solution
- Implement Auth with role claims (seeker|employer).
- Provide resume upload endpoint + parsing service (initial heuristic stub), persisting normalized skills.
- Build job index with normalized fields and dense embeddings; implement hybrid score combiner and expose explainability payload.
- Support apply + status lifecycle; emit events for observability.

### Scope
**In Scope (Sprint 1):** ST-001, ST-002, ST-003, ST-004, ST-005, ST-014.  
**Out of Scope (later):** Inbox UI (ST-006), Scheduling + Emails (ST-009, ST-008), Job edit/archive (ST-015), dashboards (ST-012), budgets (ST-013).

---

## Implementation Details

### Source Tree Changes (Sprint 1)
- backend/
  - app/api/v1/routes/
    - recommendations.py (NEW): list recommendations for seeker
    - uploads.py (NEW): resume upload
  - app/services/
    - parsing_service.py (NEW): basic resume parsing
    - recommend_service.py (NEW): index + scoring + explainability
    - events.py (NEW): event logging helper
  - app/models/
    - profile.py (NEW): seeker profile fields (skills, preferences)
  - app/core/
    - errors.py (NEW): standardized error responses
- frontend/
  - app/(auth)/login/page.tsx (NEW)
  - app/(jobs)/recommendations/page.tsx (NEW) — simple list view

### Technical Approach
- Resume Parsing (ST-002): accept PDF/DOCX; stub reads text and extracts skills via simple keyword list; persist to Profile
- Index + Embeddings (ST-003): build ChromaDB collection for jobs (title+desc+skills); create normalization tables
- Hybrid Scoring (ST-004): BM25 score + cosine similarity weighted blend; weights configurable
- Explainability (ST-005): include top n skills/terms contributing to score in response
- Apply & Status (ST-014): create Application on apply; PATCH status endpoint already present
- Events (FR-009): log key actions using app/services/events.py (JSON structured)

### Integration Points
- Frontend uses JWT bearer to call backend routes
- Backend queries Mongo via Beanie; vectors via ChromaDB

---

## Development Context

### Relevant Existing Code
- backend/app/api/v1/routes/auth.py — register/login
- backend/app/api/v1/routes/jobs.py — list/create jobs
- backend/app/api/v1/routes/applications.py — apply, list, patch status
- backend/app/models/{user,job,application}.py — core models

### Dependencies
**Framework/Libraries:**
- FastAPI, Uvicorn, Motor, Beanie, python-jose, passlib[bcrypt], python-dotenv, ChromaDB client (to add)

**Internal Modules:**
- services: parsing_service, recommend_service, events (to add)

### Configuration Changes
- Add CHROMA_DB_PATH or connection vars
- Add EMBEDDINGS_PROVIDER (openai|local), OPENAI_API_KEY if needed

### Existing Conventions (Greenfield)
- Routes under /api/v1/{domain}
- Beanie Documents in app/models
- JWT helper in app/core/security.py

### Test Framework & Standards
- Pytest (recommended); use FastAPI TestClient for route tests
- Unit tests per service; integration tests for endpoints using temporary Mongo/Chroma

---

## Implementation Stack
- Python 3.11, FastAPI latest, Beanie latest compatible with Motor
- Node 18+, Next.js 14.2.0
- MongoDB 6.x, ChromaDB local

---

## Technical Details

### Data Models
- User(Document): { email: EmailStr, hashed_password: str, role: "seeker"|"employer" }
- Profile(Document): { user_id: str, skills: [str], location?: str, preferences?: { locations?: [str], titles?: [str] } }
- Job(Document): { title: str, description: str, location?: str, skills: [str], status: "active"|"archived" }
- Application(Document): { job_id: str, user_id: str, status: "applied|viewed|shortlisted|interview|rejected" }

### Endpoints (Sprint 1)
- Auth
  - POST /api/v1/auth/register { email, password, role } → { id, email, role }
  - POST /api/v1/auth/login { email, password } → { access_token, token_type }
- Resume Upload
  - POST /api/v1/uploads/resume multipart/form-data(file) → { parsed: { skills: [], titles: [] } }
- Recommendations
  - GET /api/v1/recommendations?user_id={id}&limit=20 → [{ job, score, explain: { skills: ["python","fastapi"], terms: ["backend"] } }]
- Jobs
  - GET /api/v1/jobs → [Job]
  - POST /api/v1/jobs { title, description, location?, skills[] } → Job
- Applications
  - POST /api/v1/applications { job_id } → Application
  - GET /api/v1/applications → [Application]
  - PATCH /api/v1/applications/{id}/status { status } → Application

### Scoring Formula (ST-004)
score = w_lex * bm25(query, job) + w_sem * cosine(emb(profile), emb(job))
- Defaults: w_lex = 0.5, w_sem = 0.5; configurable via env
- Explainability: top skills/terms from normalization/token weights

### Error Responses
- 400 validation_error, 401 unauthorized, 404 not_found, 500 server_error

---

## Development Setup

- Backend
  - cd backend; python -m venv venv; source venv/bin/activate; pip install -r requirements.txt; cp .env.example .env
  - Add CHROMA_DB_PATH, EMBEDDINGS_PROVIDER, OPENAI_API_KEY (if using OpenAI)
  - uvicorn app.main:app --reload
- Frontend
  - cd frontend; npm install; npm run dev

---

## Implementation Guide

### Setup Steps
1) Add ChromaDB client dependency and env vars  
2) Create services: parsing_service.py, recommend_service.py, events.py  
3) Add models/profile.py and migration script to backfill if needed  
4) Add routes: uploads.py, recommendations.py; wire in app.main

### Implementation Steps (mapped to stories)
- ST-001 Auth: ensure role claim in JWT; protect endpoints as needed
- ST-002 Resume: implement uploads/resume; parsing_service to extract skills
- ST-003 Index: add index builder in recommend_service; normalize and persist vectors
- ST-004 Scoring: implement hybrid combiner + config weights
- ST-005 Explain: include explain payload from token/skill contributions
- ST-014 Apply/Status: verify POST apply and PATCH status; add event logging

### Testing Strategy
- Unit: parsing_service (fixtures with sample resumes), recommend_service scoring
- Integration: uploads/resume, recommendations, applications/status
- E2E: register → login → upload → recommend → apply → status

---

## Developer Resources

### File Paths Reference
- backend/app/api/v1/routes/{auth,jobs,applications,scheduling,uploads,recommendations}.py
- backend/app/services/{parsing_service,recommend_service,events}.py
- backend/app/models/{user,job,application,profile}.py

### Key Code Locations
- Security: backend/app/core/security.py  
- DB init: backend/app/db/init_db.py

### Documentation Updates
- Update docs/PRD.md API examples as endpoints stabilize
- Update docs/architecture.md ADRs if major changes

---

## Risks & Mitigations
- Resume parsing quality — start with heuristic + allow user confirm; iterate later
- Embedding cost/latency — support local embeddings toggle
- Explainability correctness — unit test attribution outputs
- Data privacy — never expose raw resume in responses; secure storage

---

## Rollout Plan
- Internal dev with local Mongo/Chroma
- Pilot subset of users; monitor metrics (CTR, apply conversion)
- Iterate weights weekly based on feedback

---

## Backout Plan
- Feature flags for recommender and explainability
- Fallback to keyword-only search if vector service unavailable

---

## Open Questions
- Final choice of resume parser library? (tech spike)  
- UI flows for recommendation feedback (thumbs up/down) — minimal in Sprint 1?

