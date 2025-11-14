# Architecture Design Document
## JobPortal - Full-Stack Application

## 1. System Overview

JobPortal is a full-stack AI-powered job matching platform using FastAPI (backend), Next.js (frontend), MongoDB (database), and ChromaDB (vector storage).

## 2. High-Level Architecture

```
┌──────────────────────────────────────────┐
│   Frontend (Next.js 14 + TypeScript)    │
│          + Tailwind CSS                  │
└─────────────────┬────────────────────────┘
                  │ HTTPS/REST API
                  ▼
┌──────────────────────────────────────────┐
│    Backend (FastAPI + Python 3.11)      │
│  ┌────────┐  ┌────────┐  ┌──────────┐  │
│  │  Auth  │  │Business│  │ AI/ML    │  │
│  │ (JWT)  │  │ Logic  │  │(LangChain│  │
│  └────────┘  └────────┘  └──────────┘  │
└────────┬──────────────────┬─────────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│    MongoDB      │  │    ChromaDB     │
│   (Beanie)      │  │  (Embeddings)   │
└─────────────────┘  └─────────────────┘
         │                  │
         └──────┬───────────┘
                ▼
       ┌─────────────────┐
       │   OpenAI API    │
       └─────────────────┘
```

## 3. Technology Stack

**Frontend:**
- Next.js 14 (App Router), TypeScript, Tailwind CSS

**Backend:**
- FastAPI, Python 3.11, Beanie ODM, JWT auth

**Data:**
- MongoDB 7.0+, ChromaDB (vector storage)

**AI:**
- LangChain, OpenAI GPT-4, text-embedding-ada-002

**DevOps:**
- Docker, Docker Compose, structured logging

## 4. Project Structure

```
/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/v1/      # API endpoints
│   │   ├── models/      # Beanie models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── ai/          # AI/ML components
│   │   └── core/        # Config, security
│   ├── tests/           # Backend tests
│   └── requirements.txt
├── frontend/            # Next.js application
│   ├── app/            # App router pages
│   ├── components/     # React components
│   ├── lib/            # Utilities
│   └── types/          # TypeScript types
├── docs/               # Documentation
├── docker-compose.yml
└── README.md
```

## 5. API Design

**Base URL:** `/api/v1`

**Key Endpoints:**
- `POST /auth/register, /auth/login` - Authentication
- `GET,PUT /seekers/me` - Job seeker profile
- `POST /seekers/me/resume` - Resume upload
- `GET /jobs` - Job search
- `POST /applications` - Apply to job
- `POST /jobs` - Create job (employer)
- `GET /jobs/{id}/applications` - View applicants
- `POST /ai/match` - Calculate match score

## 6. AI Matching System

**Embedding Generation:**
1. Extract text from profile/job
2. Generate embedding via OpenAI (ada-002)
3. Store in MongoDB + ChromaDB

**Matching Algorithm:**
```
score = (
  semantic_similarity * 0.5 +  # Cosine similarity
  skills_match * 0.3 +         # Jaccard index
  experience_match * 0.1 +
  location_match * 0.1
) * 100
```

## 7. Security

- **Authentication:** JWT tokens (15min access, 7d refresh)
- **Authorization:** Role-based (job_seeker, employer)
- **Encryption:** bcrypt passwords, HTTPS
- **Validation:** Pydantic models
- **Rate Limiting:** Per endpoint

## 8. Deployment

**Docker Compose Services:**
- `frontend`: Next.js on port 3000
- `backend`: FastAPI on port 8000
- `mongodb`: MongoDB on port 27017
- `chromadb`: ChromaDB on port 8001

**Commands:**
```bash
docker-compose up -d
docker-compose logs -f
```

## 9. Performance & Scalability

- **Performance:** <500ms API response, <2s page load
- **Scalability:** Horizontal scaling, connection pooling
- **Caching:** Embedding cache, query results
- **Monitoring:** Structured JSON logs

## 10. Future Enhancements

- Real-time chat (WebSockets)
- Video interviews
- Mobile apps
- Advanced analytics
- Microservices migration
