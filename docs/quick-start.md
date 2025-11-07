# 🚀 Quick Start Guide - Job Portal Application

Complete guide to run the full-stack application and see the UI.

---

## Prerequisites ✅

You already have:
- ✅ Node.js v22.19.0
- ✅ Python 3.9.6
- ✅ Docker v28.0.4

---

## Step 1: Start MongoDB (Database)

MongoDB needs to be running for the backend API.

```bash
# Start MongoDB using Docker
docker run -d \
  --name job-portal-mongo \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest

# Verify it's running
docker ps | grep mongo
```

**Alternative:** If you already have MongoDB running locally, skip this step.

---

## Step 2: Setup Backend (FastAPI)

Open a **new terminal tab** for the backend:

```bash
# Navigate to backend directory
cd /Users/dre/JobPortal/asu-group-four/backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="mongodb://localhost:27017"
export DATABASE_NAME="job_portal"
export JWT_SECRET="your-secret-key-change-in-production"

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test it:** Open http://localhost:8000/docs in your browser to see the API documentation (Swagger UI).

---

## Step 3: Setup Frontend (Next.js)

Open **another new terminal tab** for the frontend:

```bash
# Navigate to frontend directory
cd /Users/dre/JobPortal/asu-group-four/frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

**Expected output:**
```
   ▲ Next.js 14.2.0
   - Local:        http://localhost:3000
   - Ready in 2.3s
```

---

## Step 4: Access the UI 🎉

Open your browser and go to:

**👉 http://localhost:3000**

You should see the Job Portal homepage!

---

## What You Can Do in the UI

Based on the implemented features, you can:

### As a Job Seeker:
1. **Register/Login** - Create account as "seeker"
2. **Upload Resume** - Upload PDF/DOCX resume
3. **View Recommendations** - See personalized job matches
4. **View Explanations** - See why jobs were recommended
5. **Apply to Jobs** - Submit applications
6. **Track Applications** - See application status

### As an Employer:
1. **Register/Login** - Create account as "employer"
2. **Post Jobs** - Create job listings
3. **View Applications** - See who applied
4. **Manage Inbox** - Smart inbox for applicants
5. **Update Status** - Change application status
6. **Schedule Interviews** - Send calendar invites

---

## Troubleshooting

### MongoDB Connection Error

**Error:** `ConnectionError: Could not connect to MongoDB`

**Fix:**
```bash
# Check if MongoDB is running
docker ps | grep mongo

# If not running, start it
docker start job-portal-mongo

# Or create new container
docker run -d --name job-portal-mongo -p 27017:27017 mongo:latest
```

### Backend Port Already in Use

**Error:** `Error: Address already in use`

**Fix:**
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Port Already in Use

**Error:** `Port 3000 is already in use`

**Fix:**
```bash
# Kill the process using port 3000
lsof -i :3000
kill -9 <PID>

# Or Next.js will ask if you want to use a different port (3001)
```

### Module Not Found Errors

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

## Quick Commands Summary

### Option 1: Using the Management Script (Recommended)

```bash
# Start everything with one command
./manage.sh start

# Check status
./manage.sh --status

# Stop everything
./manage.sh stop

# See all options
./manage.sh --help
```

### Option 2: Manual Setup (in separate terminals)

```bash
# Terminal 1: MongoDB
docker run -d --name job-portal-mongo -p 27017:27017 mongo:latest

# Terminal 2: Backend
cd backend
source venv/bin/activate
export MONGODB_URI="mongodb://localhost:27017"
uvicorn app.main:app --reload --port 8000

# Terminal 3: Frontend
cd frontend
npm run dev
```

**Access Points:**
- 🌐 **Frontend UI:** http://localhost:3000
- 📡 **Backend API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/docs
- 🗄️ **MongoDB:** localhost:27017

**📘 For detailed management options, see the [Service Management Guide](service-management-guide.md)**

---

## Environment Variables (Optional)

Create a `.env` file in the backend directory for easier configuration:

```bash
# backend/.env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=job_portal
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
RESUME_STORAGE_DIR=storage/resumes
EMBEDDINGS_PROVIDER=local
EMBEDDING_DIMENSIONS=128
SCORING_BM25_WEIGHT=0.4
SCORING_VECTOR_WEIGHT=0.6
RECOMMENDATION_LIMIT=10
EMAIL_PROVIDER=console
```

Then just run:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

---

## Stop Everything

### Using Management Script:
```bash
./manage.sh stop
```

### Manual Shutdown:
```bash
# Stop frontend (CTRL+C in Terminal 3)

# Stop backend (CTRL+C in Terminal 2)
# Then deactivate virtual environment
deactivate

# Stop MongoDB
docker stop job-portal-mongo

# Optional: Remove MongoDB container
docker rm job-portal-mongo
```

---

## Next Steps After Starting

1. **Register an account** at http://localhost:3000/register
2. **Upload a resume** (if seeker) at /profile/resume
3. **Create job postings** (if employer) at /jobs/create
4. **View recommendations** at /recommendations
5. **Test the E2E flows** described in the stories

---

## Development Tips

**Hot Reload:**
- Both frontend and backend support hot reload
- Changes are reflected automatically

**View Logs:**
- Backend logs appear in Terminal 2
- Frontend logs appear in Terminal 3
- Check browser console for frontend errors (F12)

**Database Inspection:**
```bash
# Connect to MongoDB shell
docker exec -it job-portal-mongo mongosh

# In mongosh:
use job_portal
db.users.find()
db.jobs.find()
db.applications.find()
```

---

**Ready to go!** 🚀

Open http://localhost:3000 and start exploring the Job Portal!
