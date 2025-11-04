# Backend (FastAPI) - Starter

Minimal FastAPI scaffold for Job Portal MVP.

## Quickstart

1) Create venv and install deps:
```
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

2) Set env:
```
cp .env.example .env
```

3) Run server:
```
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for Swagger UI.

## Layout
- app/main.py (app + routes mount)
- app/api/v1/routes (auth, jobs, applications)
- app/core (config, security, logging, errors)
- app/models, app/schemas (Beanie + Pydantic)
- app/db/init_db.py (Mongo init + Beanie init)

