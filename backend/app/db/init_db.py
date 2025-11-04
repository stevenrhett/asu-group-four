import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.models.profile import Profile
from app.models.event import EventLog


async def init_db():
    load_dotenv()
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DATABASE_NAME", "job_portal")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    await init_beanie(database=db, document_models=[User, Job, Application, Profile, EventLog])
