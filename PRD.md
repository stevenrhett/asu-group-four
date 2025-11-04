# Product Requirements Document (PRD) – JobPortal

## 🧭 Overview
**Project:** JobPortal  
**Methodology:** BMAD-METHOD v6  
**Owner:** Product Manager (PM Agent)  
**Version:** Draft 0.1  

JobPortal is an AI-driven job-matching platform designed to connect job seekers and employers through intelligent search, automation, and personalized recommendations.  
This document defines the functional, technical, and user-experience requirements for the MVP release.

---

## Objectives
- Enable job seekers to create profiles, upload résumés, and find relevant roles efficiently.  
- Enable employers to post jobs, review candidates, and schedule interviews.  
- Integrate AI-powered recommendation and search functions using LangChain + OpenAI.  
- Provide secure authentication and responsive, modern UI.  
- Deliver a Dockerized, full-stack web app ready for deployment.

---

## Target Users
| Persona | Description | Primary Goals |
|----------|--------------|----------------|
| **Job Seeker** | Individual searching for employment | Build profile, apply easily, receive job alerts |
| **Employer** | HR or recruiter posting jobs | Post listings, filter applicants, track hiring stages |
| **Admin (future)** | Platform operator | Manage accounts, moderate content, view analytics |

---

## Functional Requirements

### 1. Authentication & Accounts
- JWT-based login/signup for job seekers and employers  
- Password hashing with bcrypt  
- Role-based dashboard redirection  
- Profile CRUD (Create, Read, Update, Delete)

### 2. Job Management
- Employers can post, edit, and delete jobs  
- Job seekers can browse, filter, and search jobs  
- Support filters: title, skill, location, company, job type  
- Pagination and search performance under 300 ms  

### 3. Applications & Workflow
- Apply via uploaded résumé or one-click “Apply Now”  
- Track application history and status  
- Employers can review, shortlist, and schedule interviews  
- Email notifications or dashboard alerts on status change  

### 4. AI Matching & Recommendations
- Resume parsing + keyword extraction  
- Job-to-candidate vector embedding comparison (ChromaDB)  
- Personalized job suggestions (LangChain + OpenAI GPT-4o/Claude 3.x)  

### 5. System Management
- Logging of actions and system events  
- Exception handling and input validation  
- Configurable `.env` with environment-based setup  

---

## Non-Functional Requirements
- Average API response time < 300 ms  
- 99.9% uptime target (cloud deployment)  
- Scalable async backend (FastAPI + Uvicorn)  
- Database hosted on MongoDB Atlas  
- Secure communication (HTTPS, no plaintext credentials)  
- Frontend responsive for desktop + mobile  

---

## User Experience (UX)
- Clean, modern layout built with Tailwind CSS  
- Clear separation of seeker and employer flows  
- Dashboard panels for jobs, applications, and alerts  
- Dark/light mode (optional stretch goal)  
- Accessibility compliance: WCAG 2.1 AA  

---

## Future Enhancements
- OAuth (Google/LinkedIn) login  
- Resume scoring system  
- Automated job approval workflow  
- Analytics dashboard for employers  
- Chatbot for candidate-employer interaction  

---

## Deliverables (MVP)
- Working web app with full CRUD for users and jobs  
- AI job recommendation engine (prototype)  
- REST API documentation (OpenAPI/Swagger)  
- Deployed containerized app (Docker Compose)  
- Unit/integration tests + CI/CD pipeline  

---

## Milestones

| Milestone | Goal | Primary Agents |
|------------|------|----------------|
| **M1 – Setup & Auth** | Repo, environment, FastAPI + MongoDB + JWT auth | Analyst, PM, Dev |
| **M2 – Job CRUD** | Employer/Seeker job management | PM, Dev |
| **M3 – Application Flow** | Apply, track, and notify | PM, Dev |
| **M4 – AI Matching** | LangChain + embeddings integration | Architect, Dev |
| **M5 – UI & Deployment** | Next.js frontend, Docker, and release | Dev, PM |

---

## Definition of Done
- Code reviewed and merged into `main` branch  
- Unit and integration tests pass locally and in CI  
- All core features functional per requirements  
- Deployment succeeds without configuration errors  
- README, PRD, and BMAD tracking files updated  

---

> **Next step:**  
> PM Agent → Run `epics` workflow to break features into detailed user stories.  
> UX Designer → Run `ux-design` workflow if UI mockups are required.  
> Architect → Run `create-architecture` workflow to validate integration paths.
