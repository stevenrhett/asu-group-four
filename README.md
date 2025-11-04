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
