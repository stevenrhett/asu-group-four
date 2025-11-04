from fastapi import APIRouter
from typing import List

from app.models.job import Job, JobCreate

router = APIRouter()


@router.get("/", response_model=List[Job])
async def list_jobs():
    return await Job.find_all().to_list()


@router.post("/")
async def create_job(payload: JobCreate):
    job = Job(**payload.dict())
    await job.insert()
    return job

