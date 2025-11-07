# **Application Overview**

The JobPortal project aims to develop a secure, scalable, and user-friendly platform connecting job seekers and employers. The core functionalities for job seekers include creating profiles, uploading resumes, searching and applying for jobs, and receiving notifications. Employers can post jobs, review applications, schedule interviews, and communicate with candidates.

The system will also leverage AI for personalized job recommendations, resume parsing, and candidate matching.

## **Core Functional Scope**

### **Job Seeker Account**

As a job seeker, I want to:

* Register and create a profile with personal details and resume upload.  
* Login to my account securely.  
* Search jobs by title, skills, location, or company.  
* Apply for jobs with a single click or via resume submission.  
* Receive job alerts and notifications via email.  
* View application status and history.  
* Receive AI-powered job recommendations based on profile and preferences.

### **Employer Account**

As an employer, I want to:

* Register and create a company profile.  
* Post new job openings with detailed descriptions.  
* Review applications and shortlist candidates.  
* Schedule interviews and send email notifications.  
* Track applications and generate reports on candidate status.  
* Receive AI-powered candidate recommendations for posted jobs.

**Note:** Any additional features that improve user experience, engagement, or operational efficiency are encouraged

## **Definition of Done**

* Fully working application demo.  
* For MongoDB document definition remember to use the chart on this [project spec](https://github.com/ASU-Vibe-Coding-Centre/project-specs/blob/main/todo-project/todo-specs.md#database-mongodb)  
* Share code repository for technical evaluation with:  
  * ERD Diagram  
  * Architecture Diagram

## **System Expectations**

* Secure password encryption using strong hashing algorithms.  
* JWT or equivalent token-based authentication for session management.  
* Input validation, exception handling, and logging implemented consistently.

## **Platform / Tech Stack**

* **Backend:** Python 3.11+, FastAPI (async), Uvicorn/Gunicorn  
* **Frontend:** Next.js 14 (App Router), TypeScript, React, Tailwind CSS (or equivalent design system)  
* **Database:** MongoDB 6.x (Atlas or managed); Pydantic \+ Beanie ODM  
* **Vector Store:** ChromaDB  
* **AI Orchestration:** LangChain for prompt chains, tools, retrieval pipelines, n8n  
* **Models:** OpenAI (GPT-4o/4.1) or Anthropic Claude 3.x/4; OpenAI text-embedding-3-small for embeddings; fallback to open-source (all-MiniLM-L6-v2)  
* **Containerization:** Docker.  
* **Observability:** Structured logging

#### **Frontend Walkthrough**

The Job Portal frontend should be built with **Next.js (App Router)** and follows a **modular, feature-based architecture**:

* **app/** – Defines routes and layouts for pages like Home, Login, Dashboard, and nested routes.  
* **components/** – Contains global, reusable UI components such as buttons, cards, and navigation bars.  
* **features/** – Encapsulates each feature (auth, dashboard, job listings) with its own components, hooks, API services, and state management.  
* **hooks/** – Houses global reusable React hooks for data fetching, debouncing, etc.  
* **lib/** – Utilities, shared API clients, and helper functions.  
* **store/** – Global state management (Redux/Zustand) for authentication, UI, and other app-wide state.  
* **types/ & constants/** – Centralized TypeScript types/interfaces and app-wide constants.  
* **services/ & middleware/** – Shared services like logging, analytics, and middleware for authentication.  
* **styles/ & public/** – Global CSS/Tailwind styles and static assets.  
* **tests/ & scripts/** – Unit/integration tests and utility scripts for build/deploy.

This structure ensures scalability, maintainability, and clear separation of concerns for enterprise-level applications.

#### **Backend Walkthrough**

The Job Portal backend should be built using Python 3.11+ and FastAPI, following a modular architecture. The folder structure and responsibilities are as follows:

* **app/** – Root application folder. Contains all backend logic and modules.  
  * **main.py** – Entry point of the application, starts the FastAPI server.  
  * **api/** – Defines versioned API endpoints.  
    * **v1/routes/** – Route handlers for features like authentication, users, jobs, applications, recommendations, and AI assistant.  
    * **dependencies.py** – Common dependencies for routes (e.g., DB session, auth).  
  * **core/** – Core app configuration and utilities.  
    * config.py – Environment and application configuration.  
    * security.py – Authentication, password hashing, JWT handling.  
    * logging.py – Structured logging setup.  
    * rate\_limit.py – Rate limiting logic.  
    * errors.py – Centralized error handling.  
  * **models/** – Database models using Pydantic \+ Beanie.  
    * Examples: user.py, company.py, job.py, application.py, resume.py, conversation.py.  
  * **schemas/** – Request/response validation and serialization.  
    * Includes auth.py, user.py, job.py, application.py, resume.py, assistant.py, and common schemas.  
  * **repositories/** – Encapsulates database operations for each model.  
    * Examples: user\_repository.py, job\_repository.py, application\_repository.py, resume\_repository.py.  
  * **services/** – Business logic and domain services.  
    * Examples: authentication, resume parsing, search, recommendations, suggestions, email handling.  
  * **ai/** – AI orchestration and workflows.  
    * **providers/** – API clients for AI models (OpenAI, Anthropic).  
    * **prompts/** – System prompts and templates for AI interactions.  
    * **chains/** – LangChain prompt chains (recommendation, cover letter).  
    * **rag/** – Retrieval-Augmented Generation: loader, splitter, embeddings, vectorstore, retriever, QA chain.  
    *  **agents/** –  Agent orchestration  
  * **workers/** – Background processing.  
    * queue.py, scheduler.py – Task management and scheduling.  
    * **tasks/** – Background tasks like embedding generation and email sending.  
  * **db/** – Database setup and management.  
    * init\_db.py – Async MongoDB connection and Beanie initialization.  
    * indexes.py – Index definitions.  
    * migrations/ – Database migrations.  
  * **utils/** – Shared utilities and adapters.  
    * Examples: pagination helpers, validators, adapters for integrations.  
* **Root files** – Project-level configuration and dependencies.  
  * Dockerfile – Containerization setup.  
  * requirements.txt / pyproject.toml – Python dependencies.  
  * .env.example – Environment variables template.

Instructions

## **Open Project in Cursor IDE**

**Steps:**

1. Launch **Cursor IDE**.  
2. Use **Open Project**:  
   1. Ctrl \+ O (Windows/Linux) or Cmd \+ O (Mac)  
   2. Navigate to the **Job Portal project root folder**.  
3. Alternatively, **Clone Repository** from Git:  
   1. File \> Clone Repository  
   2. Provide repository URL and choose a local path.  
4. **Connect via SSH** (optional):  
   1. For remote development, connect using SSH to an EC2 or dev server.  
5. **Recent Projects**:  
   1. Access previously opened Job Portal project from the **Welcome Screen**.

**Cursor Context Tip:**

* Use @Files and @Folders to quickly navigate to backend/, frontend/, or any specific module.

#### **Cursor AI Config : Workflow**

Configure a structured workflow in Cursor IDE to **manage project setup, feature development, testing, and deployment** efficiently, using AI-assisted suggestions, rules, and contextual navigation.

## **1\. Workflow Using Command Prompts**

### Cursor IDE Command Prompts for Job Portal

New Projects

* Define Project Requirements Document  
  * Use @doc to reference PRD and project design notes.  
* Define Project Structure  
  * Backend: models, repositories, services, routers, db  
  * Frontend: app, components, features, hooks, store  
  * Docker: backend Dockerfile, frontend Dockerfile, docker-compose.yml  
  * Config: .env, [settings.py](http://settings.py/), tailwind.config.js

Building Features

* Implementation Plan for a Feature  
  * Use Cursor AI "Ask" or "Agent" to generate high-level implementation plan  
* Review the Implementation Plan  
  * Validate tasks, dependencies, and folder structure  
* Select Files and Implement  
  * Navigate using @Files, @Folders, @Code  
  * Use @CursorRules to enforce coding standards  
* UI/UX Guidelines  
  * Reference design files using @Docs  
  * Suggest CSS/Tailwind classes using Cursor AI  
* Manually Test the Feature  
  * Backend: test APIs via Swagger docs or Postman  
  * Frontend: test UI components in browser  
* Commit and Merge  
  * Use Cursor AI to suggest descriptive commit messages  
  * Ensure feature branch merged to main

## **2\. Recommended Cursor Workflow Prompts**

Cursor IDE supports **workflow prompts** to automate or guide repetitive tasks. Here’s how to configure them:

### **A. New Project Setup Prompt**

* **Trigger:** “Initialize Job Portal Project”  
* **Actions:**  
  * Create folder structure  
  * Generate main.py, Dockerfile, docker-compose.yml  
  * Add default .env placeholders  
  * Link PRD using @doc

### **B. Feature Implementation Prompt**

* **Trigger:** “Build Feature \<feature\_name\>”  
* **Actions:**  
  * Create models, services, and routes if backend feature  
  * Create components, hooks, and API services if frontend  
  * Apply UI/UX guidelines via @Docs or Tailwind suggestions  
  * Suggest unit tests template

### **C. Code Review Prompt**

* **Trigger:** “Review Code”  
* **Actions:**  
  * Validate Cursor rules (naming conventions, model registration)  
  * Suggest optimizations (async calls, Tailwind classes)  
  * Highlight missing environment variables or Docker mappings

### **D. Deployment Preparation Prompt**

* **Trigger:** “Prepare for Docker Deployment”  
* **Actions:**  
  * Verify Dockerfiles  
  * Check docker-compose.yml for correct env variables  
  * Suggest health checks for containers  
  * Prepare startup scripts

## **3\. Cursor Rules Integration**

* **Example Rules for Job Portal:**  
  1. **Model Registration Rule**: Every Beanie model must be added to init\_db.py.  
  2. **Environment Rule**: .env must contain MONGODB\_URI, DATABASE\_NAME, SECRET\_KEY, NEXT\_PUBLIC\_API\_URL.  
  3. **Frontend Component Rule**: All React components must have proper Tailwind classnames for padding, margin, colors, and responsive design.  
  4. **Commit Rule**: Commit messages must include feature name and JIRA/task ID if applicable.

## **4\. Cursor AI Best Practices for Workflow**

* Use **“Ask” model** for quick code snippets or validation.  
* Use **“Agent” model** for multi-step feature creation across backend and frontend.  
* Use @Files, @Folders, @Code, and @Docs extensively to maintain context.  
* Maintain a **feature-based folder organization** for scalability.  
* Regularly **update Cursor rules** to reflect coding standards and project-specific guidelines.

#### **Initializing the Project**

**Backend (FastAPI \+ Beanie \+ MongoDB)**

The backend is built using **FastAPI**, a modern, high-performance Python framework ideal for asynchronous APIs. **Beanie** is used as the ODM (Object Document Mapper) for MongoDB, providing async operations, schema validation, and automatic collection creation.

Key aspects:

* **Virtual Environment Management:** Isolated Python environment using venv ensures dependency management and avoids conflicts.  
* **Dependency Management:** All required packages are installed via requirements.txt, including FastAPI, Uvicorn (ASGI server), Beanie, Motor (MongoDB async driver), Pydantic, Passlib, and JWT libraries.  
* **Environment Configuration:** Sensitive information like database URI and secret keys are managed through .env files, ensuring security and ease of configuration.  
* **Folder Structure:** Organized into models, schemas, services, routers, db, and core to maintain separation of concerns and enforce clean architecture.  
* **Initialization:** main.py and init\_db.py ensure proper startup, database connection, and model registration.  
* **Testing:** Swagger UI (/docs) provides interactive API documentation for testing endpoints during development.

### **Frontend (Next.js \+ Tailwind CSS)**

The frontend is built with **Next.js** using the **App Router** pattern, providing a **modular, feature-based architecture** that is ideal for enterprise applications. **Tailwind CSS** ensures consistent styling, responsive design, and rapid UI development.

Key aspects:

* **Project Structure:** Organized into app (pages/routes), components (reusable UI elements), features (feature-specific components and hooks), hooks (global React hooks), lib (utilities), store (state management), styles, and public (static assets).  
* **Tailwind Integration:** Provides utility-first CSS, enabling rapid design with responsive and consistent styling for buttons, forms, cards, and layouts.  
* **TypeScript/JSX Support:** Ensures type safety, better developer experience, and maintainable code.  
* **Development Workflow:** npm run dev launches the app in development mode with hot-reloading.  
* **Scalable Component Design:** Modular feature-based architecture allows independent development of auth, dashboard, and job listings.

Instructions

## **1\. Backend – FastAPI \+ Beanie**

### **Step 1: Navigate to backend**

cd backend

### **Step 2: Set Up Python Virtual Environment**

python \-m venv venv

* Activate virtual environment:  
  * **Windows:** venv\\Scripts\\activate  
  * **Linux/Mac:** source venv/bin/activate

### **Step 3: Install Dependencies**

1. Create requirements.txt:

fastapi uvicorn beanie motor pydantic python-jose passlib\[bcrypt\]

1. Install packages:

pip install \-r requirements.txt

###  

## **2\. Frontend – Next.js \+ Tailwind CSS**

### **Step 1: Create Frontend Folder**

cd ../ npx create-next-app@latest frontend

* Choose **App Router** and **JSX**.  
* Navigate to frontend/ folder.

### **Step 2: Install Tailwind CSS**

npm install \-D tailwindcss postcss autoprefixer npx tailwindcss init \-p

###  

## **Notes**

* Always activate **Python virtual environment** before installing or running backend.  
* Keep .env secure; use .env.example for team sharing.

#### **Mongo DB Setup**

* **Cluster Creation:** Set up a cloud-hosted MongoDB cluster (M0 Free Tier for development) on your preferred cloud provider and region.  
* **Network Access:** Whitelist IP addresses to allow your application to connect securely. Options include your current IP, all IPs for development, or specific server/VPN IPs.  
* **Database User:** Create a dedicated database user with read/write privileges for your Job Portal. These credentials are stored in the .env file for secure access.  
* **Automatic Collections:** Collections are automatically created by Beanie when models are initialized in Python, so no manual setup is required.

Instructions

# **MongoDB Atlas Setup (Job Portal)**

### **Step 1: Create a Cluster**

1. Sign in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).  
2. Click **“Create Cluster”** → select cloud provider & region.  
3. Choose **M0 (Free Tier)** for development.  
4. Click **Create Cluster** and wait a few minutes.

### **Step 2: Whitelist Network Access**

1. Navigate to **Network Access → Add IP Address**.  
2. Options:  
   1. **Current IP** – automatic detection  
   2. **Anywhere** – 0.0.0.0/0 (dev only)  
   3. **Specific IP** – server/VPN IP  
3. Click **Confirm**.

### **Step 3: Create Database User**

1. Go to **Database Access → Add New Database User**.  
2. Set **username & password** (for .env).  
3. Assign **Read/Write to any database**.  
4. Save the user.

**Note:** You do **not** need to manually create collections. Beanie automatically creates collections based on your document models when you initialize them in Python.

#### **Mongo DB : Connect and operation Via Python**

The objective of this setup is to build a **scalable, type-safe, and fully asynchronous backend** for a Job Portal application using **FastAPI** and **Beanie (MongoDB ODM)**.

Key goals:

1. Establish a **robust database connection** to MongoDB with environment-based configuration.  
2. Define **Beanie document models** for all collections (Jobs, Users, Applications, etc.) with proper validation and type safety.  
3. Initialize MongoDB and Beanie efficiently at application startup.  
4. Provide a modular project structure for scalability and maintainability.  
5. Enable **async CRUD operations** and leverage FastAPI features like dependency injection and automatic OpenAPI documentation.

This setup follows a **layered, modular architecture** to ensure maintainability and extensibility.

### **1\. Environment Configuration (.env)**

* All sensitive credentials and configuration variables, like MONGODB\_URI and DATABASE\_NAME, are stored in a .env file.  
* Pydantic’s BaseSettings reads and validates these settings, ensuring **type safety** and **consistency across environments**.

### **2\. Core Settings (core/config.py)**

* Centralized configuration using Pydantic Settings.  
* Provides a single source of truth for database URIs, app name, and other environment-specific variables.  
* Supports **case-sensitive and environment-based configuration management**.

### **3\. Beanie Models (models/)**

* Each MongoDB collection is represented as a **Beanie Document**, which integrates seamlessly with FastAPI for async operations.  
* Example: Job model includes fields like title, description, company, location, skills, employment type, salary, recruiter, date posted, and status.  
* Includes **default values**, **optional fields**, and **type validation**.  
* Automatically creates collections in MongoDB when initialized.

### **4\. Database Initialization (db/init\_db.py)**

* Uses **AsyncMongoClient** for the MongoDB client and Beanie’s init\_beanie for model registration.  
* Centralizes DB initialization to ensure a **single database instance** across the application.  
* Provides a get\_database helper for direct MongoDB operations (e.g., GridFS) outside of Beanie.

### **5\. FastAPI App Startup (main.py)**

* FastAPI application is initialized with a **startup event** to initialize the database.  
* Ensures the database and Beanie models are ready before processing any API requests.  
* This enables **async CRUD operations** to be performed safely on all models.

Instructions

#  **Python FastAPI \+ Beanie Integration (Job Portal)**

### **Step 1: .env Configuration**  

MONGODB\_URI=mongodb+srv://\<username\>:\<password\>@cluster0.abcd.mongodb.net/job\_portal\_db?retryWrites=true\&w=majority\&appName=job-portal  
DATABASE\_NAME=job\_portal\_db

### **Step 2: Core Settings (core/config.py)**

from pydantic\_settings import BaseSettings  
from pydantic import Field

class Settings(BaseSettings):  
    app\_name: str \= "Job Portal App"  
    mongodb\_uri: str \= Field(..., alias="MONGODB\_URI")  
    database\_name: str \= Field(..., alias="DATABASE\_NAME")

    class Config:  
        env\_file \= ".env"  
        case\_sensitive \= True

settings \= Settings()

### **Step 3: Define Beanie Models (models/)**

Create models for each collection:

Example (**models/job.py**):

from beanie import Document  
from pydantic import BaseModel, Field  
from typing import List, Optional  
from datetime import datetime

class Job(Document):  
    title: str \= Field(..., description="Job title")  
    description: str \= Field(..., description="Full job description")  
    company: str \= Field(..., description="Company offering the job")  
    location: str \= Field(..., description="Job location (city, country)")  
    skills: List\[str\] \= Field(default\_factory=list, description="Required skills")  
    employment\_type: Optional\[str\] \= Field(default="Full-time", description="Full-time, Part-time, Contract, Internship")  
    salary\_min: Optional\[float\] \= Field(None, description="Minimum salary")  
    salary\_max: Optional\[float\] \= Field(None, description="Maximum salary")  
    posted\_by: str \= Field(..., description="User ID of recruiter")  
    date\_posted: datetime \= Field(default\_factory=datetime.utcnow, description="Date the job was posted")  
    status: str \= Field(default="active", description="Job status: active, closed, draft")

    class Settings:  
        name \= "jobs"

**Tip:** Beanie automatically creates these collections in MongoDB when initialized.

### **Step 4: Database Initialization (db/init\_db.py)**

from pymongo import AsyncMongoClient  
from beanie import init\_beanie  
from src.core.config import settings  
from src.models.user import User  
from src.models.job import Job  
from src.models.application import Application  
from src.models.category import Category  
from src.models.tag import Tag  
from src.models.comment import Comment

\_database \= None  \# Global DB instance

async def init\_db():  
    """  
    Initialize MongoDB connection and register Beanie document models.  
    """  
    global \_database

    client \= AsyncMongoClient(settings.mongodb\_uri)  
    db \= client.get\_default\_database()

    \_database \= db

    await init\_beanie(  
        database=db,  
        document\_models=\[User, Job, Application, Category, Tag, Comment\]  
    )

    print("MongoDB and Beanie initialized successfully.")

async def get\_database():  
    """  
    Get the database instance for direct MongoDB operations (GridFS, etc.)  
    """  
    global \_database  
    if \_database is None:  
        client \= AsyncIOMotorClient(settings.mongodb\_uri)  
        \_database \= client.get\_default\_database()  
    return \_database

### **Step 5: FastAPI App Startup (main.py)**

from fastapi import FastAPI  
from src.db.init\_db import init\_db

app \= FastAPI(title="Job Portal App")

@app.on\_event("startup")  
async def startup\_event():  
    await init\_db()

#### **Backend : API Building**

##  

The goal is to build a **well-structured, maintainable FastAPI backend** with:

1. Clear separation of concerns.  
2. Type-safe models using **Pydantic \+ Beanie**.  
3. Layered architecture for scalability and testability.  
4. Integration with MongoDB for persistence.  
5. Interactive API testing using **Swagger/OpenAPI**.

## **Overview**

This project is structured using a **layered architecture pattern**:

**Flow:**

**Schema (Models) → Repository → Service → Routes → main.py → Swagger Testing**

### **Layers Explained**

1. **Schema (Models)**  
   1. Defines the data structure and validation rules.  
   2. Uses **Beanie Documents** for MongoDB and **Pydantic models** for request/response validation.  
   3. Ensures type safety and consistent data modeling.  
2. **Repository Layer**  
   1. Encapsulates all database interactions.  
   2. Handles CRUD operations.  
   3. Ensures **Single Responsibility Principle (SRP)** — the repository only knows how to persist/retrieve data.  
3. **Service Layer**  
   1. Implements business logic.  
   2. Orchestrates repository calls, applies transformations, and prepares responses.  
   3. Decouples business rules from database operations, following **Service Layer pattern**.  
4. **Routes / API Layer**  
   1. Exposes endpoints to clients.  
   2. Handles HTTP requests, validation, and exception handling.  
   3. Maps endpoints to corresponding service methods, enforcing **Controller pattern**.  
5. **Main Application (main.py)**  
   1. Initializes FastAPI app, MongoDB connection, and Beanie.  
   2. Registers all routes.  
   3. Acts as the **Composition Root**, wiring all layers together.  
6. **Swagger/OpenAPI**  
   1. Auto-generated interactive documentation.  
   2. Allows testing all endpoints directly from the browser.  
   3. Provides clear request/response schemas and validation feedback.

## **Design Patterns Applied**

1. **Layered Architecture** – Separates concerns across models, repository, service, and routes.  
2. **Repository Pattern** – Abstracts database interactions from business logic.  
3. **Service Layer Pattern** – Encapsulates business rules, making logic reusable and testable.  
4. **Dependency Injection (DI)** – Services and repositories can be injected into routes (optional for more advanced setup).  
5. **Data Validation / DTO Pattern** – Pydantic models act as Data Transfer Objects (DTOs) to enforce type safety.

Instructions

# **FastAPI Backend Demo: Job Management Example**

##  

## **1\. Define the Schema**

Using **Beanie \+ Pydantic**:

\# src/schemas/job.py

from pydantic import BaseModel, Field  
from typing import List, Optional  
from datetime import datetime  
from bson import ObjectId

class JobCreate(BaseModel):  
    title: str  
    description: str  
    company: str  
    location: str  
    skills: List\[str\] \= \[\]  
    employment\_type: Optional\[str\] \= "Full-time"  
    salary\_min: Optional\[float\]  
    salary\_max: Optional\[float\]

class JobUpdate(BaseModel):  
    title: Optional\[str\]  
    description: Optional\[str\]  
    location: Optional\[str\]  
    skills: Optional\[List\[str\]\]  
    employment\_type: Optional\[str\]  
    salary\_min: Optional\[float\]  
    salary\_max: Optional\[float\]  
    status: Optional\[str\]

class JobResponse(BaseModel):  
    id: str  
    title: str  
    description: str  
    company: str  
    location: str  
    skills: List\[str\]  
    employment\_type: str  
    salary\_min: Optional\[float\]  
    salary\_max: Optional\[float\]  
    posted\_by: str  
    date\_posted: datetime  
    status: str

    class Config:  
        orm\_mode \= True,

 

## **2\. Repository Layer**

Encapsulates all DB operations:

\# src/repository/job\_repository.py  
from src.models.job import Job  
from typing import List, Optional  
from beanie import PydanticObjectId

class JobRepository:

    async def create\_job(self, job: Job) \-\> Job:  
        await job.insert()  
        return self.\_serialize\_job(job)

    async def get\_job(self, job\_id: str) \-\> Optional\[Job\]:  
        job \= await Job.get(PydanticObjectId(job\_id))  
        if job:  
            return self.\_serialize\_job(job)  
        return None

    async def get\_all\_jobs(self) \-\> List\[Job\]:  
        jobs \= await Job.find\_all().to\_list()  
        return \[self.\_serialize\_job(job) for job in jobs\]

    async def update\_job(self, job\_id: str, data: dict) \-\> Optional\[Job\]:  
        job \= await Job.get(PydanticObjectId(job\_id))  
        if job:  
            await job.update({"$set": data})  
            return self.\_serialize\_job(job)  
        return None

    async def delete\_job(self, job\_id: str) \-\> bool:  
        job \= await Job.get(PydanticObjectId(job\_id))  
        if job:  
            await job.delete()  
            return True  
        return False

    \# \------------------------  
    \# Helper method to convert ObjectId to str  
    \# \------------------------  
    def \_serialize\_job(self, job: Job) \-\> Job:  
        job.id \= str(job.id)  \# Convert ObjectId to string  
        return job

## **3\. Service Layer**

Business logic layer :

\# src/services/job\_service.py  
from src.repositories.job\_repository import JobRepository  
from src.models.job import Job  
from src.schemas.job import JobCreate, JobUpdate

class JobService:  
    def \_\_init\_\_(self):  
        self.repo \= JobRepository()

    async def create\_job(self, data: JobCreate, posted\_by: str) \-\> Job:  
        job \= Job(\*\*data.dict(), posted\_by=posted\_by)  
        return await self.repo.create\_job(job)

    async def get\_job(self, job\_id: str) \-\> Job:  
        return await self.repo.get\_job(job\_id)

    async def list\_jobs(self):  
        return await self.repo.get\_all\_jobs()

    async def update\_job(self, job\_id: str, data: JobUpdate):  
        return await self.repo.update\_job(job\_id, data.dict(exclude\_unset=True))

    async def delete\_job(self, job\_id: str):  
        return await self.repo.delete\_job(job\_id)

## **4\. Routes (API Endpoints):**

\# srcapi/v1//routes/job.py

from fastapi import APIRouter, Depends, HTTPException  
from typing import List  
from src.services.job\_service import JobService  
from src.schemas.job import JobCreate, JobUpdate, JobResponse

router \= APIRouter(prefix="/jobs", tags=\["Jobs"\])  
service \= JobService()

@router.post("/", response\_model=JobResponse)  
async def create\_job(job: JobCreate):  
    return await service.create\_job(job, posted\_by="recruiter\_id\_123")

@router.get("/", response\_model=List\[JobResponse\])  
async def list\_jobs():  
    return await service.list\_jobs()

@router.get("/{job\_id}", response\_model=JobResponse)  
async def get\_job(job\_id: str):  
    job \= await service.get\_job(job\_id)  
    if not job:  
        raise HTTPException(status\_code=404, detail="Job not found")  
    return job

@router.put("/{job\_id}", response\_model=JobResponse)  
async def update\_job(job\_id: str, job: JobUpdate):  
    updated\_job \= await service.update\_job(job\_id, job)  
    if not updated\_job:  
        raise HTTPException(status\_code=404, detail="Job not found")  
    return updated\_job

@router.delete("/{job\_id}")  
async def delete\_job(job\_id: str):  
    success \= await service.delete\_job(job\_id)  
    if not success:  
        raise HTTPException(status\_code=404, detail="Job not found")  
    return {"status": "deleted"}

## **5\. Update main.py to and add routes**

from fastapi import FastAPI  
from src.db.init\_db import init\_db  
from src.api.v1.routes import jobs

app \= FastAPI(title="Job Portal App")

@app.on\_event("startup")  
async def startup\_event():  
    await init\_db()

app.include\_router(jobs.router)

## **6\. Start FastAPI App**

uvicorn main:app \--reload

* The server will run at http://127.0.0.1:8000  
* \--reload enables live reload during development.

 

## **7\. Test Endpoints Using Swagger Docs**

* Open http://127.0.0.1:8000/docs in your browser.  
* You’ll see all routes (/jobs/, /jobs/{job\_id}, etc.) with **interactive API testing**.  
* You can create, read, update, and delete jobs directly from the browser.

#### **Backend: User Auth**

The goal is to implement **secure user authentication** for the Job Portal backend using:

* **Beanie** for MongoDB user documents.  
* **Pydantic schemas** for request/response validation.  
* **Password hashing and JWT** for secure authentication.  
* **FastAPI OAuth2 flow** for login and protected routes.  
* **A modular layered architecture**: Models → Repository → Service → Routes → Utils.  
  * **Repository layer** abstracts all direct database interactions.  
  * **Service layer** focuses solely on business logic and uses the repository.

### **Key Components**

**1\. User Model (src/models/user.py)**

* Defines user attributes: first\_name, last\_name, email, hashed\_password, role, created\_at.  
* Beanie Document ensures async database operations.  
* Automatically creates the users collection in MongoDB.

**2\. User Role Enum (src/models/enums.py)**

* Enum for user roles (e.g., recruiter, applicant).  
* Enables role-based access control if required in the future.

**3\. Schemas (src/schemas/user.py)**

* UserCreate – for registration requests.  
* UserLogin – for login requests.  
* UserResponse – for returning user info safely without exposing passwords.

**4\. Security Utils (src/utils/security.py)**

* Password hashing and verification with passlib.  
* JWT token creation and decoding for authentication.  
* Dependency functions for FastAPI routes to get the current user (get\_current\_user) from token.

**5\. Repository Layer (planned, src/repositories/user\_repository.py)**

* Encapsulates all database operations such as creating a user or fetching by email.  
* Enables unit testing by mocking database operations.  
* Service layer calls the repository for all DB interactions.

**6\. Service Layer (src/services/user\_service.py)**

* Handles CRUD operations and business logic for user management.  
* Delegates all database access to the repository layer.  
* Optional role-based checks for endpoints (e.g., recruiter/admin).

**7\. Routes (src/routers/user\_router.py)**

* /register – registers a new user via the service layer.  
* /login – authenticates user and returns JWT token.  
* /profile – protected route to get current user info.  
* /logout – frontend removes token (stateless backend).

**8\. Integration with main.py**

* Include the user router in FastAPI

Instructions

## **1\. src/models/enums.py**

from enum import Enum

class UserRole(str, Enum):  
    recruiter \= "recruiter"  
    applicant \= "applicant"

## **2\.  src/models/user.py**

from beanie import Document  
from pydantic import EmailStr, Field  
from datetime import datetime  
from .enums import UserRole

class User(Document):  
    first\_name: str  
    last\_name: str  
    email: EmailStr  
    hashed\_password: str  
    role: UserRole \= Field(default=UserRole.applicant)  
    created\_at: datetime \= Field(default\_factory=datetime.utcnow)

    class Settings:  
        name \= "users"

## **3\.  src/schemas/user.py**

from pydantic import BaseModel, EmailStr  
from datetime import datetime  
from src.models.enums import UserRole  
from typing import Optional

class UserCreate(BaseModel):  
    first\_name: str  
    last\_name: str  
    email: EmailStr  
    password: str

class UserLogin(BaseModel):  
    email: EmailStr  
    password: str

class UserResponse(BaseModel):  
    id: str  
    first\_name: str  
    last\_name: str  
    email: EmailStr  
    role: UserRole  
    created\_at: datetime

## **4\.  src/utils/security.py**

from passlib.context import CryptContext  
from datetime import datetime, timedelta  
from fastapi.security import OAuth2PasswordBearer  
from fastapi import Depends, HTTPException, status  
from jose import JWTError  
from src.models.user import User

import jwt

SECRET\_KEY \= "rev--secret-key"  
ALGORITHM \= "HS256"  
ACCESS\_TOKEN\_EXPIRE\_MINUTES \= 30

pwd\_context \= CryptContext(schemes=\["bcrypt"\], deprecated="auto")  
oauth2\_scheme \= OAuth2PasswordBearer(tokenUrl="/users/login")

\# \-------------------------------  
\# Password Utilities  
\# \-------------------------------  
def hash\_password(password: str) \-\> str:  
    return pwd\_context.hash(password)

def verify\_password(plain: str, hashed: str) \-\> bool:  
    return pwd\_context.verify(plain, hashed)

\# \-------------------------------  
\# JWT Utilities  
\# \-------------------------------  
def create\_access\_token(data: dict, expires\_delta: timedelta \= None):  
    to\_encode \= data.copy()  
    expire \= datetime.utcnow() \+ (expires\_delta or timedelta(minutes=ACCESS\_TOKEN\_EXPIRE\_MINUTES))  
    to\_encode.update({"exp": expire})  
    return jwt.encode(to\_encode, SECRET\_KEY, algorithm=ALGORITHM)

def decode\_token(token: str):  
    return jwt.decode(token, SECRET\_KEY, algorithms=\[ALGORITHM\])

\# \-------------------------------  
\# Authentication Utilities  
\# \-------------------------------  
async def authenticate\_user(email: str, password: str):  
    user \= await User.find\_one(User.email \== email)  
    if not user or not verify\_password(password, user.hashed\_password):  
        return False  
    return user

async def get\_current\_user(token: str \= Depends(oauth2\_scheme)):  
    credentials\_exception \= HTTPException(  
        status\_code=status.HTTP\_401\_UNAUTHORIZED,  
        detail="Invalid token or authentication credentials",  
        headers={"WWW-Authenticate": "Bearer"},  
    )  
    try:  
        payload \= decode\_token(token)  
        email: str \= payload.get("sub")  
        if email is None:  
            raise credentials\_exception  
        user \= await User.find\_one(User.email \== email)  
        if user is None:  
            raise credentials\_exception  
        return user  
    except JWTError:  
        raise credentials\_exception

## **5\. src/services/user\_repository.py**

from src.models.user import User  
from typing import Optional

class UserRepository:

    @staticmethod  
    async def create(user: User) \-\> User:  
        await user.insert()  
        return user

    @staticmethod  
    async def get\_by\_email(email: str) \-\> Optional\[User\]:  
        return await User.find\_one(User.email \== email)

## **6\. src/services/user\_service.py**

from src.schemas.user import UserCreate  
from src.models.user import User  
from src.utils.security import hash\_password  
from src.repositories.user\_repository import UserRepository

class UserService:

    @staticmethod  
    async def register\_user(user\_create: UserCreate) \-\> User:  
        hashed\_pw \= hash\_password(user\_create.password)  
        user\_doc \= User(  
            first\_name=user\_create.first\_name,  
            last\_name=user\_create.last\_name,  
            email=user\_create.email,  
            hashed\_password=hashed\_pw  
        )  
        return await UserRepository.create(user\_doc)

    @staticmethod  
    async def get\_user\_by\_email(email: str) \-\> User:  
        return await UserRepository.get\_by\_email(email)

## **7\. src/routers/user.py**

from fastapi import APIRouter, Depends, HTTPException  
from fastapi.security import OAuth2PasswordRequestForm  
from src.schemas.user import UserCreate, UserResponse  
from src.services.user\_service import UserService  
from src.models.user import User  
from src.utils.security import authenticate\_user, create\_access\_token, get\_current\_user

router \= APIRouter(prefix="/users", tags=\["Users"\])

@router.post("/register", response\_model=UserResponse)  
async def register\_user(user: UserCreate):  
    user\_doc \= await UserService.register\_user(user)  
    return UserResponse(  
        id=str(user\_doc.id),  
        first\_name=user\_doc.first\_name,  
        last\_name=user\_doc.last\_name,  
        email=user\_doc.email,  
        role=user\_doc.role,  
        created\_at=user\_doc.created\_at  
    )

@router.post("/login")  
async def login(form\_data: OAuth2PasswordRequestForm \= Depends()):  
    user \= await authenticate\_user(form\_data.username, form\_data.password)  
    if not user:  
        raise HTTPException(status\_code=400, detail="Invalid credentials")  
    token \= create\_access\_token(data={"sub": user.email})  
    return {"access\_token": token, "token\_type": "bearer"}

@router.get("/profile", response\_model=UserResponse)  
async def get\_profile(current\_user: User \= Depends(get\_current\_user)):  
    return UserResponse(  
        id=str(current\_user.id),  
        first\_name=current\_user.first\_name,  
        last\_name=current\_user.last\_name,  
        email=current\_user.email,  
        role=current\_user.role,  
        created\_at=current\_user.created\_at  
    )

@router.post("/logout")  
async def logout(current\_user: User \= Depends(get\_current\_user)):  
    \# Frontend removes token. Backend is stateless.  
    return {"message": "Logged out successfully"}

## **6\.  main.py (Modification)**

from fastapi import FastAPI  
from src.db.init\_db import init\_db  
from src.api.v1.routes import jobs  
from src.api.v1.routes import user

app \= FastAPI(title="Job Portal App")

@app.on\_event("startup")  
async def startup\_event():  
    await init\_db()

app.include\_router(jobs.router)  
app.include\_router(user.router) \# add user route

**This completes a ready-to-run User Auth module**:

* **Registration** → /users/register  
* **Login** → /users/login (returns JWT)  
* **Profile** → /users/profile (protected)  
* **Logout** → /users/logout

**Note:**

* **Model Registration:** Always add new Beanie models (e.g., User, Job) to document\_models in init\_db.py  
* **Testing with Swagger:** Use /docs to test register, login, profile, and logout endpoints; use **Authorize** to test token-protected routes.

#### **Frontend: UI Componenets Building**

## **Objective**

* Build and enhance the **Job Portal frontend components**.  
* Integrate backend features safely.  
* Use **Cursor AI in context** to generate, refactor, and improve code.  
* Follow **enterprise-ready UI/UX rules** and modular architecture.

Instructions

## **Step 1: Open Project in Cursor IDE**

1. Open Cursor IDE.  
2. Open your project folder: File → Open Folder → \<job-portal-path\>.  
3. Confirm your AI model selection:  
   1. **Ask** → quick fixes or code snippets.  
   2. **Agent** → multi-step tasks (components \+ routes \+ backend integration).

## **Step 2: Set Project Context**

Provide **Cursor AI** with context for your project files and rules:  

@Files src/app/layout.jsx, src/app/page.jsx, src/components/Navbar.jsx, src/components/Footer.jsx, src/components/JobCard.jsx @Files src/features/auth/LoginForm.jsx, src/features/auth/RegisterForm.jsx @Docs docs/UI\_UX.md @Cursor Rules @Past Chats

This ensures Cursor AI **understands your component structure, backend models, and UI/UX rules**.

## **Step 3: Build Frontend Components**

### **3a. Navbar Component**

Ask Cursor AI:

“Generate a responsive Navbar with Login/Register links, enterprise styling, and Tailwind classes.”

It can auto-generate Navbar.jsx with:

* Shadow, borders, padding.  
* Hover states and responsive alignment.

### **3b. JobCard Component**

Ask:

“Create a JobCard for job listings with title, company, location, skills, apply button, responsive grid layout.”

Cursor AI can produce:

* Cards with **consistent padding, shadow, and hover effects**.  
* Proper responsive design (sm:grid-cols-2, lg:grid-cols-3).

### **3c. Forms (Login / Register)**

Ask:

“Generate LoginForm/RegisterForm components with Tailwind styling, validation, and enterprise spacing.”

Cursor AI ensures:

* Input focus rings (focus:ring-primary).  
* Rounded borders and consistent padding.  
* Error message placeholders.

## **Step 4: Integrate Backend Context**

Provide Cursor AI context of **User model, routes, and services**:  

@Files src/models/user.py, src/schemas/user.py, src/services/user\_service.py, src/routers/user\_router.py @Docs docs/API\_endpoints.md @Cursor Rules

Ask Cursor AI:

“Generate API service hooks for Login/Register to call FastAPI endpoints and handle JWT token.”

## **Step 5: Update Layout & Apply Styles**

Ask Cursor AI:

“Integrate Navbar and Footer into RootLayout.jsx, apply global Tailwind enterprise styles, and ensure container padding is consistent.”

It can produce:

* Responsive layout with flex-grow main area.  
* Consistent spacing and color palette.  
* Ready-to-use layout for all pages.

## **Step 6: Test Frontend & Backend Together**

1. Run FastAPI backend:

uvicorn src.main:app \--reload

1. Run Next.js frontend:

npm run dev

1. Navigate to **Swagger UI** for API testing (http://localhost:8000/docs).  
2. Open the browser for **Home, Login, Register pages** and check:  
   1. Responsive grids for job cards.  
   2. Styled forms with hover/focus effects.  
   3. Navbar/Footer consistency.

## **Step 7: Iterative Enhancements with Cursor AI**

* Use **@Symbols** to refer to new files/components.  
* Ask Cursor AI to **refactor code, suggest new features, or update styling**.  
* Examples:  
  * “Refactor JobCard.jsx for mobile-first layout with Tailwind.”  
  * “Generate recruiter dashboard placeholder with stats cards.”  
  * “Add new job filtering component with enterprise styling.”

Cursor AI uses **project context and rules**, so all changes **follow the architecture and UI/UX guidelines**.

#### **rontend: User Auth**

# **User Authentication in Next.js**

## **1\. Architecture Overview**

In a Next.js frontend integrated with a FastAPI backend:

1. **Frontend Pages/Components** handle **user input**:  
   1. LoginForm / RegisterForm for collecting credentials.  
   2. Forms are styled with Tailwind CSS for enterprise-level design.  
2. **API Service Layer** interacts with the backend:  
   1. Sends requests to FastAPI endpoints (/users/register, /users/login).  
   2. Receives JWT tokens and user data.  
3. **State Management / Session Handling** stores authentication state:  
   1. JWT token is saved in localStorage (or cookies for more secure storage).  
   2. Protected routes check token validity before rendering.  
4. **Protected Pages** redirect unauthorized users:  
   1. If no token is present, user is redirected to /login.  
   2. Authenticated users can access /dashboard or /profile.

## **2\.  User Registration Flow**

1. **User Input**: User fills the registration form (first name, last name, email, password).  
2. **Form Submission**: Login/Register form component calls registerUser() from lib/api.js.  
3. **Backend Processing**:  
   1. FastAPI endpoint /users/register receives data.  
   2. Password is hashed with bcrypt using **passlib**.  
   3. Beanie model User saves the new user document in MongoDB.  
4. **Response**:  
   1. Backend returns user ID and basic info (without password).  
   2. Frontend can display a success message and redirect to /login.

## **3\.  User Login Flow**

1. **User Input**: Email and password are entered into LoginForm.  
2. **Form Submission**: Frontend calls loginUser() function, sending credentials to /users/login.  
3. **Backend Verification**:  
   1. FastAPI verifies email exists.  
   2. Password is checked against hashed password using verify\_password.  
   3. On success, backend generates a **JWT token** using create\_access\_token().  
4. **Token Storage**:  
   1. Frontend stores token in **localStorage**.  
   2. Token can be decoded or sent with every protected API call in the Authorization: Bearer \<token\> header.

## **4\. Protected Routes and Dashboard**

1. **Token Check**:  
   1. On page load, useEffect or a custom hook checks localStorage for a token.  
   2. If token is absent, redirect user to /login.  
2. **Token Validation**:  
   1. Optionally, call backend /users/profile endpoint with token to verify validity.  
   2. Decoded token can provide user info (e.g., first\_name, role) for personalized dashboard content.  
3. **Access Control**:  
   1. Only authenticated users can access /dashboard, /profile, or recruiter-only pages.  
   2. Unauthorized access triggers a redirect or error message.

## **5\. JWT Handling in Next.js**

* **JWT Creation (Backend)**: FastAPI signs user info (sub: email) with HS256 algorithm and secret key.  
* **JWT Storage (Frontend)**:  
  * localStorage (simple, persists across sessions).  
  * Optional: secure HTTP-only cookies (more secure against XSS).  
* **JWT Verification (Backend)**:  
  * Every protected endpoint decodes JWT to verify identity.  
  * Invalid/expired tokens return 401 Unauthorized.  
* **Frontend Usage**:

Attach token to headers when calling protected endpoints:    
fetch(\`${API\_URL}/jobs\`,   
    {   
       headers: {   
           Authorization: \`Bearer ${token}\`   
       },   
    }

* );  
   

## **6\.  Form Validation & Security**

1. **Frontend Validation**:  
   1. Required fields, email format, password strength.  
   2. Real-time error messages.  
2. **Backend Validation**:  
   1. Ensures no duplicate emails.  
   2. Password is securely hashed.  
   3. Role-based access (optional for recruiters/admin).  
3. **Security Measures**:  
   1. HTTPS communication between frontend and backend.  
   2. Token expiry for sessions (e.g., 30 mins).  
   3. Optional refresh token flow for long sessions.

## **7\. Component & State Architecture**

* **Form Components**:  
  * LoginForm.jsx and RegisterForm.jsx handle local state and form submission.  
* **API Layer (lib/api.js)**:  
  * Centralized API calls for authentication.  
* **Routing & Navigation**:  
  * useRouter() handles redirects after login/register.  
* **Protected Pages**:  
  * Dashboard and Profile components check token before rendering.  
* **Global Auth State**:  
  * Optional: Redux/Zustand for storing auth info, user profile, or permissions.

Instructions

## **Step 1: Project Context in Cursor IDE**

Open your Job Portal frontend in **Cursor IDE** and set project context:

@Files src/app/login/page.jsx, src/app/register/page.jsx, src/features/auth/LoginForm.jsx, src/features/auth/RegisterForm.jsx, src/lib/api.js  
@Docs docs/UI\_UX.md  
@Cursor Rules  
@Past Chats

* Cursor AI can now **generate or enhance forms, API calls, and components** following your **UI/UX rules**.  
* Use **“Ask”** for small snippets and **“Agent”** for multi-step tasks (e.g., form \+ API integration).

## **Step 2: Create API Service for Authentication**

### src/lib/api.js

This file contains helper functions to call FastAPI endpoints:

export const API\_URL \= "http://localhost:8000"; // FastAPI backend URL

export async function registerUser(userData) {  
  const res \= await fetch(\`${API\_URL}/users/register\`, {  
    method: "POST",  
    headers: { "Content-Type": "application/json" },  
    body: JSON.stringify(userData),  
  });  
  return res.json();  
}

export async function loginUser(userData) {  
  const res \= await fetch(\`${API\_URL}/users/login\`, {  
    method: "POST",  
    headers: { "Content-Type": "application/x-www-form-urlencoded" },  
    body: new URLSearchParams(userData),  
  });  
  return res.json();  
}

**Cursor AI Tip:**

* You can ask Cursor AI to **auto-generate this file** with proper error handling and response parsing.

## **Step 3: LoginForm Component**

### src/features/auth/LoginForm.jsx

import React, { useState } from "react";  
import { loginUser } from "../../lib/api";

export default function LoginForm({ onLoginSuccess }) {  
  const \[email, setEmail\] \= useState("");  
  const \[password, setPassword\] \= useState("");  
  const \[error, setError\] \= useState("");

  const handleSubmit \= async (e) \=\> {  
    e.preventDefault();  
    try {  
      const response \= await loginUser({ username: email, password });  
      if (response.access\_token) {  
        localStorage.setItem("token", response.access\_token);  
        onLoginSuccess();  
      } else {  
        setError("Invalid credentials");  
      }  
    } catch (err) {  
      setError("Login failed. Try again.");  
    }  
  };

  return (  
    \<form  
      onSubmit={handleSubmit}  
      className="bg-white shadow-md rounded-lg p-8 max-w-md mx-auto"  
    \>  
      \<h2 className="text-2xl font-bold mb-6 text-secondary"\>Login\</h2\>  
      {error && \<p className="text-danger mb-4"\>{error}\</p\>}  
      \<label className="block mb-2 text-gray-700"\>Email\</label\>  
      \<input  
        type="email"  
        value={email}  
        onChange={(e) \=\> setEmail(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<label className="block mb-2 text-gray-700"\>Password\</label\>  
      \<input  
        type="password"  
        value={password}  
        onChange={(e) \=\> setPassword(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<button  
        type="submit"  
        className="w-full bg-primary text-white py-2 rounded hover:bg-blue-700 transition"  
      \>  
        Login  
      \</button\>  
    \</form\>  
  );  
}

**Cursor AI Usage:**

* Ask Cursor AI to **auto-generate the form** including validation and Tailwind styling.  
* Provide context (@Cursor Rules \+ backend endpoints) to make sure it matches your backend API.

## **Step 4: RegisterForm Component**

### src/features/auth/RegisterForm.jsx

import React, { useState } from "react";  
import { registerUser } from "../../lib/api";

export default function RegisterForm({ onRegisterSuccess }) {  
  const \[firstName, setFirstName\] \= useState("");  
  const \[lastName, setLastName\] \= useState("");  
  const \[email, setEmail\] \= useState("");  
  const \[password, setPassword\] \= useState("");  
  const \[error, setError\] \= useState("");

  const handleSubmit \= async (e) \=\> {  
    e.preventDefault();  
    try {  
      const response \= await registerUser({  
        first\_name: firstName,  
        last\_name: lastName,  
        email,  
        hashed\_password: password, // backend will hash it  
      });  
      if (response.id) {  
        onRegisterSuccess();  
      } else {  
        setError("Registration failed");  
      }  
    } catch (err) {  
      setError("Error registering user");  
    }  
  };

  return (  
    \<form  
      onSubmit={handleSubmit}  
      className="bg-white shadow-md rounded-lg p-8 max-w-md mx-auto"  
    \>  
      \<h2 className="text-2xl font-bold mb-6 text-secondary"\>Register\</h2\>  
      {error && \<p className="text-danger mb-4"\>{error}\</p\>}  
      \<input  
        type="text"  
        placeholder="First Name"  
        value={firstName}  
        onChange={(e) \=\> setFirstName(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<input  
        type="text"  
        placeholder="Last Name"  
        value={lastName}  
        onChange={(e) \=\> setLastName(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<input  
        type="email"  
        placeholder="Email"  
        value={email}  
        onChange={(e) \=\> setEmail(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-4 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<input  
        type="password"  
        placeholder="Password"  
        value={password}  
        onChange={(e) \=\> setPassword(e.target.value)}  
        className="w-full border border-gray-300 rounded px-4 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-primary"  
        required  
      /\>  
      \<button  
        type="submit"  
        className="w-full bg-primary text-white py-2 rounded hover:bg-blue-700 transition"  
      \>  
        Register  
      \</button\>  
    \</form\>  
  );  
}

**Cursor AI Tip:**

* Provide @Files and @Docs context so AI **generates error handling and reusable inputs** automatically.

## **Step 5: Pages Integration**

### **Login Page (src/app/login/page.jsx)**

import LoginForm from "../../features/auth/LoginForm";  
import { useRouter } from "next/navigation";

export default function LoginPage() {  
  const router \= useRouter();

  const handleLoginSuccess \= () \=\> {  
    router.push("/dashboard");  
  };

  return \<LoginForm onLoginSuccess={handleLoginSuccess} /\>;  
}

### **Register Page (src/app/register/page.jsx)**

import RegisterForm from "../../features/auth/RegisterForm";  
import { useRouter } from "next/navigation";

export default function RegisterPage() {  
  const router \= useRouter();

  const handleRegisterSuccess \= () \=\> {  
    router.push("/login");  
  };

  return \<RegisterForm onRegisterSuccess={handleRegisterSuccess} /\>;  
}

## **Step 6: Protected Routes**

Example for a **Dashboard page**:

"use client";  
import { useEffect, useState } from "react";  
import { useRouter } from "next/navigation";

export default function DashboardPage() {  
  const router \= useRouter();  
  const \[user, setUser\] \= useState(null);

  useEffect(() \=\> {  
    const token \= localStorage.getItem("token");  
    if (\!token) router.push("/login");  
    // optionally decode token or fetch user profile  
  }, \[\]);

  return user ? \<div\>Welcome, {user.first\_name}\</div\> : null;  
}

## **Step 7: Run & Test**

1\. Start **FastAPI backend**:

uvicorn src.main:app \--reload

2\. Start **Next.js** **frontend**:

npm run dev

npm run dev

1. Navigate to /register → register a new user.  
2. Navigate to /login → login using new credentials.  
3. Verify redirect to /dashboard and token is stored in localStorage.  
4. Use **Cursor AI** to iteratively **improve forms, validation, and styling**.

#### **Assemble and & containerize the project using docker**

## **Key Concepts**

### **Containers vs Virtual Machines**

* **Containers** are lightweight, share the host OS kernel, and start instantly.  
* **VMs** include a full OS, are heavier, and take longer to provision.  
* Containers allow you to run backend, frontend, and MongoDB independently but connected via **Docker networks**.

### **Dockerfile**

* Defines **how to build a container image**.  
* Specifies **base image, dependencies, working directory, build commands, and start commands**.  
* Example:  
  * Backend: Python \+ FastAPI \+ Beanie  
  * Frontend: Node.js \+ Next.js \+ Tailwind CSS

### **Docker Compose**

* Orchestrates **multiple containers** as a single application stack.  
* Defines **services, networks, ports, and environment variables**.  
* Enables **dependency management** (depends\_on) and **volume persistence** for databases.

### **Environment Variables**

* Store **configuration, secrets, and runtime options**.  
* Example:  
  * Backend: MongoDB URI, secret keys, token expiry  
  * Frontend: API URL for dynamic content fetching  
  * MongoDB: root username/password, database name

### **Networking**

* Containers communicate via **service names** defined in Docker Compose.  
* Example: Backend connects to MongoDB using mongo:27017.  
* Frontend fetches API from backend using http://backend:8000.

## **Benefits**

* **Portability**: Runs consistently on any system with Docker installed.  
* **Isolation**: Services are independent; changes in one container don’t affect others.  
* **Scalability**: Can scale frontend/backend independently by increasing container replicas.  
* **Simplified DevOps**: Easy integration with CI/CD pipelines.  
* **Rapid Setup**: Spin up the full stack with docker-compose up \--build.  
* **Security**: Secrets can be managed via environment variables or Docker secrets.

## **Best Practices**

* **Use Multi-Stage Builds**: Reduce image size for frontend production.  
* **Separate Dev/Prod Configurations**: Use .env files or Compose overrides.  
* **Persistent Volumes**: For databases to prevent data loss on container restart.  
* **Health Checks**: Ensure containers are running correctly before connecting dependent services.  
* **Networking**: Use bridge networks for inter-container communication.  
* **Secret Management**: Avoid hardcoding sensitive keys; use environment variables or Docker secrets.  
* **Cursor AI Tip**: Use Cursor IDE to **generate Dockerfiles, Compose files, and environment templates** automatically based on project context.

Instructions

## **Step 1: Dockerfile – Backend (FastAPI \+ Beanie)**

Create backend/Dockerfile:

FROM python:3.11-slim

\# Set working directory  
WORKDIR /app

\# Install system dependencies (optional: build tools if you have dependencies like numpy, pandas etc.)  
RUN apt-get update && apt-get install \-y \--no-install-recommends \\  
    build-essential \\  
    && rm \-rf /var/lib/apt/lists/\*

\# Install Python dependencies  
COPY requirements.txt .  
RUN pip install \--no-cache-dir \-r requirements.txt

\# Copy application code  
COPY . .

\# Expose the port FastAPI runs on  
EXPOSE 8000

\# Set the entrypoint  
CMD \["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"\]

* \--reload is optional for development; remove for production.  
* Make sure requirements.txt includes FastAPI, Beanie, Motor, Passlib, python-jose, etc.

## **Step 2: Dockerfile – Frontend (Next.js \+ Tailwind CSS)**

Create frontend/Dockerfile:

\# Frontend Dockerfile for Next.js  
FROM node:18-alpine AS base

\# Install dependencies only when needed  
FROM base AS deps  
\# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3\#nodealpine to understand why libc6-compat might be needed.  
RUN apk add \--no-cache libc6-compat  
WORKDIR /app

\# Install dependencies based on the preferred package manager  
COPY package.json package-lock.json\* ./  
RUN npm ci

\# Rebuild the source code only when needed  
FROM base AS builder  
WORKDIR /app  
COPY \--from=deps /app/node\_modules ./node\_modules  
COPY . .

\# Next.js collects completely anonymous telemetry data about general usage.  
\# Learn more here: https://nextjs.org/telemetry  
\# Uncomment the following line in case you want to disable telemetry during the build.  
ENV NEXT\_TELEMETRY\_DISABLED 1

RUN npm run build

\# Production image, copy all the files and run next  
FROM base AS runner  
WORKDIR /app

ENV NODE\_ENV production  
\# Uncomment the following line in case you want to disable telemetry during runtime.  
ENV NEXT\_TELEMETRY\_DISABLED 1

RUN addgroup \--system \--gid 1001 nodejs  
RUN adduser \--system \--uid 1001 nextjs

\# COPY \--from=builder /app/public ./public

\# Set the correct permission for prerender cache  
RUN mkdir .next  
RUN chown nextjs:nodejs .next

\# Automatically leverage output traces to reduce image size  
\# https://nextjs.org/docs/advanced-features/output-file-tracing  
COPY \--from=builder \--chown=nextjs:nodejs /app/.next/standalone ./  
COPY \--from=builder \--chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000  
\# set hostname to localhost  
ENV HOSTNAME "0.0.0.0"

\# server.js is created by next build from the standalone output  
\# https://nextjs.org/docs/pages/api-reference/next-config-js/output  
CMD \["node", "server.js"\]

* npm run dev can be used for development.  
* npm start runs the built production app.

## **Step 3: Docker Compose**

Create docker-compose.yml at the project root:

services:  
  mongo:  
    image: mongo:6  
    container\_name: mongodb  
    restart: unless-stopped  
    ports:  
      \- "27017:27017"  
    volumes:  
      \- mongo\_data:/data/db  
    environment:  
      MONGO\_INITDB\_DATABASE: job\_portal\_db  
      MONGO\_INITDB\_ROOT\_USERNAME: root  
      MONGO\_INITDB\_ROOT\_PASSWORD: example  
    command: \["mongod", "--auth", "--bind\_ip\_all", "--quiet"\]  
    healthcheck:  
      test: \["CMD", "mongosh", "--eval", "db.adminCommand('ping')", "--quiet"\]  
      interval: 15s  
      timeout: 10s  
      retries: 10  
      start\_period: 40s

  backend:  
    build:  
      context: ./backend  
      dockerfile: Dockerfile  
    container\_name: fastapi-backend  
    ports:  
      \- "8000:8000"  
    environment:  
      \- MONGODB\_URI=mongodb://root:example@mongo:27017/job\_portal\_db?authSource=admin  
    depends\_on:  
      mongo:  
        condition: service\_healthy  
      redis:  
        condition: service\_healthy  
    restart: unless-stopped

  frontend:  
    build:  
      context: ./frontend  
      dockerfile: Dockerfile  
    container\_name: nextjs-frontend  
    ports:  
      \- "3001:3000"  
    environment:  
      \- NEXT\_PUBLIC\_API\_BASE\_URL=http://backend:8000  
    depends\_on:  
      backend:  
        condition: service\_started  
    restart: unless-stopped

volumes:  
  mongo\_data:

**Key points:**

* Backend and frontend are on the same Docker network .  
* Frontend accesses backend using the service name (http://backend:8000).  
* MongoDB runs in its own container with persistent volume (mongo\_data).  
* Environment variables passed via .env for backend and NEXT\_PUBLIC\_API\_URL for frontend.

  **Host the Project in AWS EC2**

  ### **Amazon EC2 (Elastic Compute Cloud)**

* **EC2** is a cloud service from AWS that provides **resizable virtual servers** in the cloud.  
* You can launch instances (virtual machines) with a specific OS, CPU, memory, and storage.  
* EC2 instances can run applications like your Job Portal backend and frontend.  
* Key features:  
  * **Elastic**: Scale resources up/down as needed.  
  * **Customizable**: Choose OS, instance type, storage, and networking.  
  * **Secure**: Control access using security groups and key pairs.

  ### **Security Groups**

* **Virtual firewalls** that control **inbound and outbound traffic** to EC2 instances.  
* Define **allowed ports, protocols, and IP addresses**.  
* For our Job Portal:  
  * Allow **SSH (port 22\)** to connect to the instance.  
  * Allow **HTTP (port 3000\)** for frontend access.  
  * Allow **HTTP (port 8000\)** for backend API/Swagger docs if needed.  
* Example rule set:

| Type | Protocol | Port Range | Source |
| :---- | :---- | :---- | :---- |
| SSH | TCP | 22 | Your IP |
| Custom TCP | TCP | 3000 | 0.0.0.0/0 |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 |

  Instructions

  ## **1\. Steps to Launch an EC2 Instance (Ubuntu)**

1. **Sign in to AWS Console** → Navigate to **EC2 Dashboard** → Click **Launch Instance**.  
2. **Choose Amazon Machine Image (AMI)** → Select **Ubuntu Server 22.04 LTS**.  
3. **Choose Instance Type** → For testing: t2.micro (free tier eligible). For production: t3.medium or higher.  
4. **Configure Instance** → Use default VPC/subnet or custom. Enable Auto-assign Public IP.  
5. **Add Storage** → Default 8GB is fine for testing; increase for production.  
6. **Add Tags** → Optional, e.g., Name \= JobPortalServer.  
7. **Configure Security Group**:  
   1. Create new security group or select existing.  
   2. Add inbound rules for SSH (22), frontend (3000), backend (8000).  
   3. Source: restrict SSH to your IP for security; frontend/backend can be 0.0.0.0/0 for public access.  
8. **Review & Launch** → Create a new **Key Pair (.pem)** → Download it securely. You will use this to SSH into the instance.  
9. **Launch Instance** → Wait until the instance state is **running**.

   ## **2\. Connect to EC2 via SSH**

**Open a terminal and execute the commands:**

* \# Set permissions for key  
* chmod 400 your-key.pem  
*   
* \# Connect to instance  
* ssh \-i your-key.pem ubuntu@\<EC2\_PUBLIC\_IP\>

  ## **3\. Install Docker on Ubuntu EC2**

1. **Update package index**:

sudo apt update && sudo apt upgrade \-y

       2\. **Follow the docker instllation in ubuntu guide** \- [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

 

## **4\. Pull Job Portal Repo and Setup**

1. **Clone the repository**:

git clone \<your-repo-url\> cd \<repo-folder\>

       2\. **Optional: adjust environment variables** in docker-compose.yml if needed.

       **3\. Run Docker Compose**:

* docker-compose up \--build \-d

* \-d runs containers in the background (detached mode).  
* This will start **MongoDB**, **backend**, and **frontend** containers.

 

## **5\. Accessing the App**

* **Frontend**: http://\<EC2\_PUBLIC\_IP\>:3000  
* **Backend Swagger docs**: http://\<EC2\_PUBLIC\_IP\>:8000/docs  
* Verify that **user registration, login, and job listings** work correctly.  
* 

