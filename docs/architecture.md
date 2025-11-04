# Architecture

## Executive Summary

Thin, scalable web architecture for a two-sided job marketplace: Next.js (App Router) frontend, FastAPI backend, MongoDB (Beanie ODM) for operational data, and ChromaDB for embeddings to power explainable hybrid recommendations. Security via JWT + bcrypt; observability and email/scheduling integrated behind provider-agnostic abstractions.

Project initialized with minimal, working scaffolds for backend and frontend.

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
| -------- | -------- | ------- | ------------- | --------- |
| Frontend | Next.js App Router + TS | 14.2.0 | Auth, Onboarding, Inbox | Mature SSR/ISR, great DX, easy API integration |
| Styling | (later) Tailwind CSS | n/a | All UI epics | Speed + consistency; easy componentization |
| Backend | FastAPI (async) | latest | Auth, RecSys, Apply, Inbox | Simple, high-perf, OpenAPI out-of-box |
| Auth | JWT (HS256) + bcrypt | n/a | Auth, Apply, Inbox | Standard, stateless, role claim support |
| DB (OLTP) | MongoDB + Beanie | 6.x | Onboarding, Jobs, Applications | Flexible schema, async ODM, quick iteration |
| Vector Store | ChromaDB | latest | Recommendations v1 | Simple local vectors; compatible with OpenAI embeddings |
| Recommender | Hybrid BM25 + Embeddings | v1 | Recommendations v1 | Balances recall/precision; explainable payload |
| Email | Provider abstraction (e.g., SendGrid) | n/a | Notifications, Scheduling | Swappable, templated messages |
| Scheduling | ICS generation | RFC 5545 | Scheduling | Interoperable invites across clients |
| Deployment | Local dev; containers later | n/a | All | Fast feedback now; containerize when integrating CI/CD |

## Project Structure

```
repo/
├─ backend/
│  ├─ app/
│  │  ├─ api/v1/routes/
│  │  │  ├─ auth.py
│  │  │  ├─ jobs.py
│  │  │  ├─ applications.py
│  │  │  └─ scheduling.py
│  │  ├─ core/{config.py,security.py}
│  │  ├─ db/init_db.py
│  │  └─ models/{user.py,job.py,application.py}
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ app/{layout.tsx,page.tsx}
│  ├─ package.json
│  ├─ tsconfig.json
│  └─ next.config.js
└─ docs/
   ├─ PRD.md
   ├─ epics.md
   ├─ sprint-status.yaml
   └─ stories/*.md
```

## Epic to Architecture Mapping

| Epic | Key Components | Notes |
| ---- | --------------- | ----- |
| Authentication & Roles | backend/app/api/v1/routes/auth.py; User model; JWT | Role claim `seeker|employer` in token |
| Onboarding & Profile | Resume parsing service (TBD), User profile fields | Normalized skills feed recommendations |
| Recommendations v1 | Job index + embeddings; scoring combiner | Exposes explainability payload |
| Employer Inbox & Scheduling | applications routes; scheduling routes; ICS util | Filters, shortlist, schedule invites |
| Notifications | Email abstraction + templates | Status-change and scheduling emails |
| Observability & Metrics | Event logging; dashboards (TBD) | CTR on recs, applies, time-to-shortlist |

## Technology Stack Details

### Core Technologies

- Frontend: Next.js 14.2.0, React 18
- Backend: FastAPI, Uvicorn, Pydantic, Beanie (Mongo), Motor
- Vector: ChromaDB; embeddings (OpenAI or local) configurable
- Auth: python-jose (JWT), passlib[bcrypt]

### Integration Points

- Frontend → Backend: REST JSON over HTTP (fetch), JWT bearer
- Backend → MongoDB: Motor async client via Beanie
- Backend → ChromaDB: Python client (index build + query)
- Backend → Email: provider abstraction (SendGrid-compatible), templated messages
- Backend → ICS: pure-Python minimal generator (upgradeable to robust lib)

## Implementation Patterns

- Routes: versioned under `/api/v1/*`; nouns + actions via HTTP verbs
- Models: Beanie `Document` for persistence + Pydantic schemas for payloads
- Services: thin service/helpers per vertical (auth, recsys, scheduling)
- Explainability: include top contributing skills/terms in recommendation response
- Feedback: thumbs up/down endpoint to log relevance signals
- Status: enum lifecycle for applications: applied → viewed → shortlisted → interview → rejected

## Consistency Rules

### Naming Conventions

- Files: kebab-case for docs, snake_case for Python modules, PascalCase for React components
- IDs: story IDs `ST-###`; FR IDs `FR-###`

### Code Organization

- Backend api: `app/api/v1/routes/{domain}.py`
- Backend models: `app/models/{entity}.py`
- Frontend pages: `/app/*` (App Router) with co-located components where helpful

### Error Handling

- Raise HTTPException with clear messages; do not expose internals
- Validate payloads with Pydantic; strict types

### Logging Strategy

- Structured logs (JSON) at backend; event logs for key funnels (clicks, applies, feedback, shortlist)

## Data Architecture

- User: { email, hashed_password, role }
- Job: { title, description, location?, skills[] }
- Application: { job_id, user_id, status }
- Relationships: User(1) — (N)Application(N) — (1)Job
- Indexing: jobs and (optionally) seeker vectors indexed in ChromaDB; alias tables for skills/titles normalization

## API Contracts

- Auth
  - POST /api/v1/auth/register — payload: { email, password, role }
  - POST /api/v1/auth/login — payload: { email, password } → { access_token }
- Jobs
  - GET /api/v1/jobs — list
  - POST /api/v1/jobs — payload: { title, description, location?, skills[] }
- Applications
  - POST /api/v1/applications — payload: { job_id }
  - GET /api/v1/applications — list
  - PATCH /api/v1/applications/{id}/status — payload: { status }
- Scheduling
  - POST /api/v1/scheduling — payload: { title, start_iso, end_iso, location?, attendees[] }
  - PUT /api/v1/scheduling/{id} — same payload
  - DELETE /api/v1/scheduling/{id}

## Security Architecture

- JWT bearer auth; `sub` (user id), `role` claims
- Password hashing via bcrypt
- Input validation; deny by default for protected routes
- Future: rate limits and audit logs for sensitive ops

## Performance Considerations

- Async IO across DB and HTTP
- Query indexes on common fields (job title, skills)
- Recommender: batched embeddings; weighted score with configurable params; P95 < 400ms target
- Caching (future): hot job lists, profile-derived queries

## Deployment Architecture

- Local dev: `uvicorn app.main:app --reload` and `next dev`
- Containers (future): Dockerfiles for backend and frontend; docker-compose for Mongo + services
- Environments: `.env` for backend; secrets manager for production

## Development Environment

### Prerequisites

- Python 3.11+, Node 18+, MongoDB (local or Atlas), Optional: ChromaDB server

### Setup Commands

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Architecture Decision Records (ADRs)

- ADR-001: Choose Next.js App Router for frontend SSR/SPA flexibility
- ADR-002: Use FastAPI + Beanie + MongoDB for rapid iteration and async performance
- ADR-003: Implement hybrid recommender (BM25 + embeddings) with explainability
- ADR-004: Use JWT with role claims for simple, stateless auth
- ADR-005: Generate ICS invites with a minimal utility; abstract email provider

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: 2025-11-04_
_For: Team 4_

