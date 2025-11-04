from fastapi import APIRouter, HTTPException
from typing import List, Literal
from pydantic import BaseModel

from app.models.application import Application, ApplicationCreate
from app.models.job import Job

router = APIRouter()


@router.post("/")
async def apply(payload: ApplicationCreate):
    job = await Job.get(payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    app = Application(job_id=str(job.id), user_id="TBD")  # TODO: derive from auth context
    await app.insert()
    return app


@router.get("/", response_model=List[Application])
async def list_applications():
    return await Application.find_all().to_list()


class StatusUpdate(BaseModel):
    status: Literal["applied", "viewed", "shortlisted", "interview", "rejected"]


@router.patch("/{application_id}/status")
async def update_status(application_id: str, payload: StatusUpdate):
    app = await Application.get(application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = payload.status
    await app.save()
    return app
