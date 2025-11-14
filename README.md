# JobPortal - AI-Powered Job Matching Platform

An intelligent job matching platform that connects job seekers with employers using AI-powered recommendations, semantic search, and automated matching algorithms.

## 🚀 Features

### For Job Seekers
- **AI-Powered Job Matching**: Get personalized job recommendations based on your profile
- **Profile Management**: Create comprehensive profiles with resume upload
- **Smart Job Search**: Search and filter jobs by location, type, salary, and more
- **One-Click Applications**: Apply to jobs quickly and easily
- **Real-Time Tracking**: Track application status with instant notifications
- **Job Alerts**: Set up alerts for new matching opportunities

### For Employers
- **Job Posting Management**: Create and manage job postings easily
- **AI-Ranked Candidates**: Get candidates ranked by match score
- **Applicant Review**: Review applicant profiles and resumes
- **Interview Scheduling**: Schedule and manage interviews
- **Analytics**: Track views and applications for your postings

### AI Features
- **Semantic Matching**: Uses OpenAI embeddings for intelligent job-candidate matching
- **Resume Parsing**: Automatic extraction of skills and experience
- **Match Scoring**: 0-100% compatibility scores with detailed explanations
- **Vector Search**: Fast semantic search powered by ChromaDB

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (Next.js 14 + TypeScript)   │
│          + Tailwind CSS                 │
└────────────────┬────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────┐
│    Backend (FastAPI + Python 3.11)     │
│  ┌────────┐  ┌────────┐  ┌──────────┐ │
│  │  Auth  │  │Business│  │ AI/ML    │ │
│  │ (JWT)  │  │ Logic  │  │(LangChain│ │
│  └────────┘  └────────┘  └──────────┘ │
└────────┬──────────────────┬────────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│    MongoDB      │  │    ChromaDB     │
│   (Beanie)      │  │  (Embeddings)   │
└─────────────────┘  └─────────────────┘
```

## 📋 Prerequisites

- **Docker & Docker Compose** (Recommended)
  - OR -
- **Python 3.11+**
- **Node.js 20+**
- **MongoDB 7.0+**
- **OpenAI API Key** (for AI features)

## 🚀 Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/stevenrhett/asu-group-four.git
cd asu-group-four
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
- **Required**: Set `OPENAI_API_KEY` with your OpenAI API key
- **Important**: Change `SECRET_KEY` to a secure random string
- Optional: Adjust other settings as needed

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017
- **ChromaDB**: localhost:8001

### 4. Access the Application

Open your browser and navigate to:
- **Main App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

### 5. Stop Services

```bash
docker-compose down
```

To remove all data:
```bash
docker-compose down -v
```

## 🛠️ Manual Installation (Development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp ../.env.example .env
# Edit .env with your settings

# Start MongoDB and ChromaDB separately or via Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0
docker run -d -p 8001:8000 --name chromadb chromadb/chroma:latest

# Run the backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run the frontend
npm run dev
```

## 📚 API Documentation

### Authentication Endpoints

```
POST /api/v1/auth/register - Register new user
POST /api/v1/auth/login    - Login user
GET  /api/v1/auth/me       - Get current user
```

### Job Seeker Endpoints

```
GET  /api/v1/seekers/me          - Get profile
PUT  /api/v1/seekers/me          - Update profile
POST /api/v1/seekers/me/resume   - Upload resume
```

### Employer Endpoints

```
GET  /api/v1/employers/me - Get employer profile
PUT  /api/v1/employers/me - Update employer profile
```

### Job Endpoints

```
GET  /api/v1/jobs           - Search jobs
GET  /api/v1/jobs/{id}      - Get job details
POST /api/v1/jobs           - Create job (employer)
PUT  /api/v1/jobs/{id}      - Update job (employer)
GET  /api/v1/jobs/my-jobs   - Get my jobs (employer)
```

### Application Endpoints

```
POST /api/v1/applications           - Apply to job
GET  /api/v1/applications           - Get my applications
GET  /api/v1/applications/{id}      - Get application details
```

For detailed API documentation, visit http://localhost:8000/docs after starting the backend.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🏗️ Project Structure

```
asu-group-four/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── ai/             # AI/ML components
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Backend tests
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   └── types/             # TypeScript types
├── docs/                  # Documentation
│   ├── PRD.md            # Product Requirements
│   ├── ERD.md            # Database Schema
│   └── ARCHITECTURE.md   # Architecture Design
├── docker-compose.yml    # Docker orchestration
└── .env.example         # Environment template
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**:
- `MONGODB_URL`: MongoDB connection string
- `SECRET_KEY`: JWT secret key
- `OPENAI_API_KEY`: OpenAI API key (required)
- `CHROMA_HOST`: ChromaDB host
- `DEBUG`: Debug mode (True/False)

**Frontend (.env.local)**:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 🤖 AI Matching Algorithm

The platform uses a multi-factor matching algorithm:

1. **Semantic Similarity (50%)**: Cosine similarity of job and profile embeddings
2. **Skills Match (30%)**: Jaccard similarity of required vs. possessed skills
3. **Experience Level (10%)**: Match between job requirements and candidate experience
4. **Location Preference (10%)**: Alignment of location preferences

Final score: 0-100% compatibility with detailed explanation.

## 📊 Database Schema

### Collections:
- **users**: User accounts and authentication
- **job_seeker_profiles**: Job seeker profiles and preferences
- **employer_profiles**: Employer/company profiles
- **jobs**: Job postings
- **applications**: Job applications and status
- **notifications**: User notifications

See [docs/ERD.md](docs/ERD.md) for detailed schema.

## 🔒 Security Features

- JWT-based authentication with access and refresh tokens
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Input validation with Pydantic
- CORS configuration
- Rate limiting (production)
- Secure file upload handling

## 🚢 Deployment

### Docker Production Deployment

1. Build production images:
```bash
docker-compose -f docker-compose.yml build
```

2. Run with production environment:
```bash
docker-compose up -d
```

### Manual Production Deployment

1. Set `DEBUG=False` in backend .env
2. Use production-grade WSGI server (e.g., Gunicorn)
3. Set up reverse proxy (Nginx)
4. Use managed MongoDB (MongoDB Atlas)
5. Set up SSL/TLS certificates
6. Configure proper secrets management

## 📝 Development Guidelines

### Backend Code Style
- Black formatter
- Flake8 linter
- Type hints required
- Docstrings for all functions

### Frontend Code Style
- ESLint + Prettier
- TypeScript strict mode
- Component documentation

## 🐛 Troubleshooting

### "Connection refused" error
- Ensure all services are running: `docker-compose ps`
- Check MongoDB is accessible: `docker logs jobportal-mongodb`

### "OpenAI API error"
- Verify OPENAI_API_KEY is set in .env
- Check API key has sufficient credits

### Frontend can't reach backend
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS origins in backend config

### Port already in use
- Change ports in docker-compose.yml
- Or stop conflicting services

## 📖 Additional Documentation

- [Product Requirements Document](docs/PRD.md)
- [Entity Relationship Diagram](docs/ERD.md)
- [Architecture Design](docs/ARCHITECTURE.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is part of ASU Group Four coursework.

## 👥 Team

Virtual Team using BMAD-METHOD:
- **Analyst**: Requirements gathering and user research
- **Product Manager**: Feature prioritization and roadmap
- **Architect**: System design and technical decisions
- **Developer**: Implementation and testing

## 🙏 Acknowledgments

- OpenAI for GPT and embedding models
- FastAPI framework
- Next.js framework
- MongoDB and ChromaDB
- Tailwind CSS

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `/docs`
- Review API docs at `/docs` endpoint

---

**Happy Job Hunting! 🎯**
