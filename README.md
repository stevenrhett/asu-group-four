# Job Portal - AI-Powered Job Matching Platform

An intelligent job matching platform that connects job seekers with employers using hybrid AI-powered recommendations combining BM25 text matching and semantic embeddings.

## ✨ Features

### For Job Seekers
- 🔐 Secure authentication with JWT
- 📄 Resume upload and automatic parsing (PDF/DOCX)
- 🎯 AI-powered job recommendations based on skills and experience
- 📊 View recommendation scores with explanations
- 🔍 Browse and apply to job postings

### For Employers
- 🏢 Create and manage job postings
- 📥 Smart inbox with AI-assisted candidate filtering
- 📧 Application status notifications
- 📅 Interview scheduling with calendar invites
- 🎯 View candidate match scores

## 🚀 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js 14, React, TypeScript |
| **Backend** | FastAPI (Python 3.11+), Uvicorn |
| **Database** | MongoDB + Beanie ODM |
| **AI/ML** | Sentence Transformers, BM25 |
| **Authentication** | JWT, bcrypt |
| **Testing** | Pytest, Playwright, Jest |
| **Deployment** | Docker |

## 📋 Key Features

- **Hybrid Scoring System**: Combines BM25 text matching with semantic embeddings for accurate recommendations
- **Resume Parsing**: Automatic extraction of skills, job titles, and experience from uploaded resumes
- **Real-time Notifications**: Email alerts for application status changes and interview invitations
- **Smart Inbox**: AI-powered filtering and ranking of job applications for employers
- **Explainability**: Clear scoring breakdown showing why jobs were recommended
- **Observability**: Comprehensive logging, metrics, and performance monitoring  

---

## 🏁 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (or Docker)

### 1. Clone the Repository
```bash
git clone https://github.com/stevenrhett/asu-group-four.git
cd asu-group-four
```

### 2. Start MongoDB
```bash
docker run -d --name job-portal-mongo -p 27017:27017 mongo:latest
```

### 3. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Setup Frontend (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Quick Start Script
```bash
chmod +x manage.sh
./manage.sh start          # Start all services
./manage.sh restart        # Restart all (auto-cleans ports!)
./manage.sh --status       # Check service status
./manage.sh stop           # Stop all services
./manage.sh --help         # See all commands
```

**✨ New:** Restart commands automatically clean up orphaned processes - no more port conflicts!

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:
- `MONGODB_URL` - MongoDB connection string
- `SECRET_KEY` - JWT secret key
- `SMTP_HOST`, `SMTP_PORT` - Email configuration
- `FRONTEND_URL` - Frontend URL for CORS

## 📚 Documentation

- � [Quick Start Guide](docs/quick-start.md) - Detailed setup instructions
- 🔧 [Service Management Guide](docs/service-management-guide.md) - Using manage.sh to control services
- 📋 [Product Requirements](docs/PRD.md) - Complete PRD
- 🏗️ [Architecture](docs/architecture.md) - System design and architecture
- 🔍 [Observability Guide](docs/observability-readme.md) - Metrics and monitoring
- 📊 [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)
- 🧪 [Testing Guide](docs/sprints/sprint-1/TEST-RUNBOOK.md) - How to run tests

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm test                           # Jest unit tests
npx playwright test               # E2E tests
```

## 📁 Project Structure

```
asu-group-four/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic (ML, parsing, email)
│   │   ├── core/        # Config, security, middleware
│   │   └── schemas/     # Pydantic schemas
│   └── tests/           # Pytest test suite
│
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   ├── e2e/            # Playwright tests
│   └── __tests__/      # Jest unit tests
│
└── docs/               # Documentation
    ├── stories/        # User stories
    └── sprints/        # Sprint deliverables
```

## 🤝 Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines.

## 👥 Team

**Arizona State University - Group 4**

- Andre Exilien
- David Nwankwo
- Muhammad Zahid
- Steven Johnson

---

**Project Repository**: [github.com/stevenrhett/asu-group-four](https://github.com/stevenrhett/asu-group-four)

---

## Team Channel

**[Team Channel – project-team-4](https://asu.enterprise.slack.com/archives/C09Q3SM2THV)**  

**Members:**  
David Nwankwo • Muhammad Zahid • Steven Johnson • Andre Exilien  

This channel includes:  
- 💬 Real-time messaging for collaboration  
- 🧭 A project overview canvas for defining scope  
- ✅ A task-tracker list for deliverables  
- 🔄 Automatic status updates linked to workflows  
- 👋 A welcome workflow for new members  

---

## Introducing BMAD-METHOD V6

###  What Is BMAD?
Think of it as having specialized consultants at every stage — planning, architecture, and development.  
Each phase has dedicated AI agents that ask the right questions, guide the process, and ensure *nothing falls through the cracks.*

### Why This Matters
- **Better Planning = Better Code** — Plan first, code faster, refactor less.  
- **Clear Handoffs** — PRDs → Architecture → Development. Everyone aligned.  
- **Faster Development** — Structured planning removes guesswork.  
- **Less AI Hallucination** — Each workflow is isolated and task-specific.  
- **Scalable** — Works for both small fixes and large-scale projects.  

---

## The Four Phases

1. **Analysis (Optional)** – Brainstorm and draft a product brief.  
2. **Planning (Required)** – Create detailed requirements or tech spec.  
3. **Architecture (Conditional)** – Define system design and components.  
4. **Implementation (Required)** – Build, test, and iterate through sprints.  

---

## The BMAD AI Team

| **Role** | **Responsibility** |
|-----------|--------------------|
| 🧪 Analyst | Kicks off workflows and tracks progress |
| 📊 Product Manager | Writes PRDs or tech specs |
| 🎨 UX Designer | Designs UI and mockups |
| 🏗️ Architect | Defines tech stack and system design |
| 🏃 Scrum Master | Runs sprints and breaks down epics |
| 👨‍💻 Developer | Builds, tests, and reviews code |

---

## Your Journey

### Getting Started
1. Analyst → `workflow-init`  
2. Describe your project  
3. System determines project level  
4. Progress file auto-created  

### Planning Phase
- PM → `prd` or `tech-spec`  
- UX Designer → `ux-design`  
- Architect → `create-architecture`  
- Architect → `solutioning-gate-check`  

### Implementation Phase
- Scrum Master → `sprint-planning`  
- For each story:  
  - `create-story`  
  - `story-context` *(optional)*  
  - Developer → `dev-story`  
  - Developer → `code-review` *(recommended)*  
- After each epic: `retrospective`  

> **Pro Tip:** Use fresh chats per task to reduce AI confusion.

---

## Keys to Success
- Use **fresh chats** for each workflow  
- Let **AI agents** auto-update tracking files  
- Trust the process — planning saves time  
- Ask any agent for `workflow-status` if unsure  
- Keep documents strong — they’re your shared language  

---

## What We’ll Create
- `bmm-workflow-status.md` – Current phase tracking  
- `PRD.md` – Product Requirements  
- `Epics.md` – Feature stories  
- `Architecture.md` – System design  
- `UX Design Document` – UI/UX layout  
- `sprint-status.yaml` – Real-time tracking  

---

## Summary
BMAD turns *“What do we build and how?”* into a structured workflow with clear roles and deliverables.  
We spend more time **thinking**, less time **guessing**.  
The AI amplifies human expertise — it doesn’t replace it.  
**Let’s build something great together.** 
