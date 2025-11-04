# Entity Relationship Diagram (ERD)
## JobPortal Database Schema

## Collections Overview

### 1. User Collection (`users`)
- _id: ObjectId (PK)
- email: String (unique, indexed)
- password_hash: String
- role: Enum["job_seeker", "employer"]
- is_active: Boolean
- created_at, updated_at: DateTime

### 2. JobSeekerProfile Collection (`job_seeker_profiles`)
- _id: ObjectId (PK)
- user_id: ObjectId (FK -> User, unique)
- first_name, last_name: String
- phone: String
- location: {city, state, country, zip_code}
- skills: [String]
- experience: [{company, title, dates, description}]
- education: [{institution, degree, dates}]
- resume: {file_name, file_path, parsed_text}
- preferences: {job_types, salary_range, locations}
- profile_embedding: [Float] (1536-dim vector)

### 3. EmployerProfile Collection (`employer_profiles`)
- _id: ObjectId (PK)
- user_id: ObjectId (FK -> User, unique)
- company_name, industry: String
- location: {address, city, state}
- description: String

### 4. Job Collection (`jobs`)
- _id: ObjectId (PK)
- employer_id: ObjectId (FK -> EmployerProfile)
- title, description: String
- skills_required: [String]
- job_type: Enum["full_time", "part_time", "contract"]
- experience_level: Enum["entry", "mid", "senior"]
- salary_min, salary_max: Integer
- location: {city, state, is_remote}
- status: Enum["active", "closed"]
- job_embedding: [Float] (1536-dim vector)
- posted_at, created_at: DateTime

### 5. Application Collection (`applications`)
- _id: ObjectId (PK)
- job_id: ObjectId (FK -> Job)
- job_seeker_id: ObjectId (FK -> JobSeekerProfile)
- status: Enum["submitted", "under_review", "interview_scheduled", "rejected", "accepted"]
- ai_match_score: Float (0-100)
- cover_letter: String
- applied_at: DateTime
- Unique constraint: (job_id, job_seeker_id)

### 6. Notification Collection (`notifications`)
- _id: ObjectId (PK)
- user_id: ObjectId (FK -> User)
- type: Enum["application_status", "new_job_match", "interview"]
- message: String
- is_read: Boolean
- created_at: DateTime

## Relationships

**One-to-One:**
- User ↔ JobSeekerProfile (role = "job_seeker")
- User ↔ EmployerProfile (role = "employer")

**One-to-Many:**
- EmployerProfile → Job
- Job → Application
- JobSeekerProfile → Application
- User → Notification

**Many-to-Many:**
- JobSeekerProfile ↔ Job (through Application)

## ERD Diagram
```
User (1:1) → JobSeekerProfile
User (1:1) → EmployerProfile
EmployerProfile (1:N) → Job
Job (1:N) → Application
JobSeekerProfile (1:N) → Application
User (1:N) → Notification
```

## AI Vector Storage
- **profile_embedding**: Generated from skills + experience + education
- **job_embedding**: Generated from title + description + requirements
- **Similarity**: Cosine similarity → ai_match_score (0-100)
