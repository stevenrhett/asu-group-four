# Job Portal: AI-Powered Job Matching Platform
## One-Page Summary

---

## Team 4 - Arizona State University
**Andre Exilien • David Nwankwo • Muhammad Zahid • Steven Johnson**

**Repository:** [github.com/stevenrhett/asu-group-four](https://github.com/stevenrhett/asu-group-four)

---

## The Problem

### Job Seekers Face:
- 📊 Information overload from hundreds of irrelevant listings
- ❓ No explanation of why jobs are recommended
- 🕳️ Black box algorithms with zero transparency
- ⏱️ Hours wasted manually filtering opportunities

### Employers Struggle With:
- 📥 200+ applications per role to manually review
- 🔍 Quality candidates buried in the noise
- ⏰ Days to weeks spent on initial screening
- 🎯 No clear way to identify top matches

---

## Our Solution

**An intelligent two-sided marketplace with transparent, AI-powered recommendations**

### Key Innovation: Hybrid AI Matching
- **BM25 Text Matching** (40%): Fast keyword precision
- **Semantic Embeddings** (60%): Contextual understanding
- **Explainability Layer**: Clear reasoning for every match

---

## Platform Features

### For Job Seekers 🎯
- **Smart Recommendations**: Personalized matches with scores and explanations
- **Intelligent Resume Parsing**: Automatic PDF/DOCX skill extraction
- **Application Tracking**: Real-time status updates and notifications

### For Employers 🏢
- **Smart Inbox**: AI-ranked candidates with match scores
- **Quick Actions**: Shortlist, reject, and schedule with one click
- **Interview Scheduling**: Automatic calendar invite generation

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14, React, TypeScript | Modern, responsive UI |
| **Backend** | FastAPI, Python 3.11+ | High-performance async API |
| **Database** | MongoDB + Beanie ODM | Flexible data modeling |
| **AI/ML** | Sentence Transformers, BM25 | Hybrid recommendations |
| **Vector Store** | ChromaDB | Semantic search |
| **Auth** | JWT + bcrypt | Secure authentication |

---

## Architecture Highlights

```
┌─────────────┐
│  Next.js UI │  ← TypeScript, React Components
└──────┬──────┘
       │ REST API + JWT
       ▼
┌─────────────┐
│  FastAPI    │  ← Async Python, Pydantic Validation
│  Backend    │
└──────┬──────┘
       │
   ┌───┴───┬──────────┐
   ▼       ▼          ▼
MongoDB  ChromaDB   SMTP
(Data)   (Vectors)  (Email)
```

**Key Principles:**
- Async I/O throughout for performance
- Clean separation of concerns
- Provider-agnostic abstractions (email, storage)
- Horizontally scalable design

---

## How the AI Works

### Hybrid Recommendation Algorithm

1. **Text Matching (BM25)**
   - Index job descriptions and resume text
   - Score based on term frequency and relevance
   - Fast and explainable

2. **Semantic Matching (Embeddings)**
   - Convert text to high-dimensional vectors
   - Measure similarity in semantic space
   - Understands context and meaning

3. **Combined Scoring**
   ```python
   final_score = (0.4 × bm25_score) + (0.6 × embedding_score)
   ```

4. **Explainability**
   - Extract top contributing skills
   - Identify matching experience levels
   - Show job title similarity
   - Return transparent breakdown to user

---

## Development Methodology: BMAD

**Building Modern AI-Driven applications**

### Four Phases:
1. **Analysis**: Brainstorming, design thinking, product brief
2. **Planning**: PRD, user stories, success criteria
3. **Architecture**: Tech decisions, system design, API contracts
4. **Implementation**: Sprint execution with testing

**Result:** Structured workflow that prevented scope creep and ensured quality

---

## Sprint 1 Deliverables

### 6 Major Epics Completed ✅

1. **Authentication & Authorization**
   - JWT-based auth with role claims (seeker/employer)
   - Secure password handling with bcrypt

2. **Resume Upload & Parsing**
   - Multi-format support (PDF/DOCX)
   - AI-powered skill and experience extraction

3. **Job Posting Management**
   - CRUD operations for employers
   - Job listing dashboard

4. **Hybrid Recommendation Engine**
   - BM25 + embeddings implementation
   - Explainability layer with scoring breakdown

5. **Application Flow**
   - One-click apply functionality
   - Status tracking (applied → viewed → shortlisted → interview → rejected)

6. **Smart Employer Inbox**
   - AI-powered candidate filtering and ranking
   - Shortlist and interview scheduling

**Plus:** Email notifications, metrics tracking, comprehensive observability

---

## Results & Performance

### Technical Metrics ✅

| Metric | Target | Achieved |
|--------|--------|----------|
| Recommendation Latency (P95) | <400ms | **350ms** |
| API Response Time (avg) | <200ms | **180ms** |
| Test Coverage | >80% | **85%** |
| Resume Parse Time | <5s | **2-3s** |

### Expected User Impact (Projected)

- **+20-30%** increase in job recommendation CTR
- **+15%** boost in application completion rate
- **>70%** relevance rating from users
- **<2 days** employer time-to-shortlist

---

## Key Differentiators

| Feature | Traditional Platforms | Our Platform |
|---------|----------------------|--------------|
| **Matching** | Keyword search only | Hybrid AI (BM25 + Embeddings) |
| **Transparency** | Black box | Explainable scoring |
| **Resume Parsing** | Manual or basic | AI-powered extraction |
| **Employer Tools** | Simple inbox | Smart filtering + ranking |
| **Trust** | Low (no explanation) | High (clear reasoning) |

---

## What We Learned

### Technical Insights
- ✅ Hybrid approach outperforms single-method AI
- ✅ Explainability builds user trust
- ✅ Async architecture crucial for performance
- ✅ Type safety (TypeScript + Pydantic) prevents bugs

### Process Insights
- ✅ BMAD structure prevented development chaos
- ✅ Planning upfront saved implementation time
- ✅ Documentation kept team aligned
- ✅ Testing early caught issues before they compounded

---

## Future Roadmap

### Phase 2: Enhanced Intelligence (3 months)
- 🧠 Learn-to-rank reranker for personalization
- 📊 Skills graph and ontology
- 📱 Mobile applications (iOS/Android)
- 🔗 ATS integration for enterprise

### Phase 3: Career Intelligence (6-12 months)
- 🤖 Career copilot for job seekers
- 📊 Real-time market intelligence
- 🎓 Skill gap analysis and training recommendations
- 💰 Salary insights and negotiation tools

### Enterprise Vision
- 🏢 White-label solutions
- 📈 Advanced analytics dashboards
- 🔐 SSO and enterprise security
- ⚡ API access and bulk operations

---

## Try It Yourself

### Quick Start
```bash
# Clone the repository
git clone https://github.com/stevenrhett/asu-group-four.git
cd asu-group-four

# Run the startup script
./start.sh

# Access the application
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (or Docker)

---

## Project Statistics

- **Lines of Code:** ~15,000+
- **Test Cases:** 50+ comprehensive tests
- **API Endpoints:** 20+ RESTful endpoints
- **Database Models:** 4 core entities (User, Job, Application, Event)
- **Documentation:** 1,000+ lines across PRD, architecture, stories

---

## Contact & Resources

### Team 4
- Andre Exilien
- David Nwankwo
- Muhammad Zahid
- Steven Johnson

### Links
- **GitHub:** [github.com/stevenrhett/asu-group-four](https://github.com/stevenrhett/asu-group-four)
- **Documentation:** See `/docs` folder in repository
- **API Docs:** http://localhost:8000/docs (when running)

### Documentation Highlights
- 📋 [Product Requirements (PRD)](docs/PRD.md)
- 🏗️ [Architecture Document](docs/architecture.md)
- 🧪 [Test Runbook](docs/sprints/sprint-1/TEST-RUNBOOK.md)
- 📊 [Implementation Summary](docs/sprints/sprint-1/implementation-summary.md)

---

## Why This Matters

**We're making job matching transparent, intelligent, and human-centered.**

### The Vision
Current job platforms treat matching as a black box. We believe users deserve to understand WHY they're seeing recommendations. By combining:

- ✨ **Modern AI** (hybrid recommendations)
- 🔍 **Transparency** (explainable scoring)
- 🎯 **User-centric design** (solving real pain points)

We're building a platform that serves both sides of the marketplace effectively.

---

## Core Philosophy

> **"AI should augment human decision-making, not replace it. Transparency builds trust. Trust builds better matches."**

---

**Thank you!** 🎉

**Questions? Let's discuss!**

---

*Presentation materials created for Arizona State University - Group 4 Project*
*Date: November 2025*
