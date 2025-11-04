# JobPortal – AI-Driven Job Matching Platform

## Overview
JobPortal is a secure, scalable, and AI-powered platform connecting job seekers and employers.  
Built using the **BMAD-METHOD (Breakthrough Method for Agile AI-Driven Development)**, the system leverages a virtual AI team — Analyst, Product Manager, Architect, and Developer — to accelerate high-quality software delivery.

**BMAD-METHOD:** [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)

---

## Core Features

### For Job Seekers
- Create an account, profile, and upload a résumé  
- Search and apply for jobs by title, skills, or company  
- View application history and receive alerts  
- AI-driven job recommendations  

### For Employers
- Register and manage company profile  
- Post and manage job listings  
- Review applications and schedule interviews  
- AI-assisted candidate matching  

---

## Technical Stack

| **Layer** | **Technology** |
|------------|----------------|
| **Frontend** | Next.js 14, React, TypeScript, Tailwind CSS |
| **Backend** | FastAPI (Python 3.11+), Uvicorn/Gunicorn |
| **Database** | MongoDB 6.x (Atlas) + Beanie ODM |
| **AI Layer** | LangChain + OpenAI (GPT-4o / Claude 3.x) + ChromaDB |
| **Auth & Security** | JWT, bcrypt, input validation, logging |
| **Deployment** | Docker + environment-based config |

---

## System Expectations
- Strong password hashing and token-based authentication  
- Consistent error handling, logging, and validation  
- Modular architecture with clear separation of concerns  

---

## Deliverables
- Working application demo  
- ERD and architecture diagrams  
- Docker setup and `.env.example`  
- Unit tests and structured logs  
- Comprehensive README and setup guide  

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/<your-user>/JobPortal.git
cd JobPortal

# Start backend
docker compose up --build

# Start frontend
npm install && npm run dev
```
⸻
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
