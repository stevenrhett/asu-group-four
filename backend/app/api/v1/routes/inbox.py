from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.api.deps import require_role
from app.models.application import Application
from app.models.job import Job
from app.models.user import User


INBOX_STATUSES = ["applied", "viewed", "shortlisted", "interview", "rejected"]


class InboxCounts(BaseModel):
    applied: int = 0
    viewed: int = 0
    shortlisted: int = 0
    interview: int = 0
    rejected: int = 0


class InboxItem(BaseModel):
    id: str
    job_title: str
    candidate_email: Optional[str]
    status: str
    updated_at: datetime


class InboxResponse(BaseModel):
    counts: InboxCounts
    items: List[InboxItem]


class StatusUpdateRequest(BaseModel):
    status: str


router = APIRouter()


@router.get("/applications", response_model=InboxResponse)
async def list_applications(
    status_filter: str = Query("all", alias="status"),
    current_user: User = Depends(require_role("employer")),
):
    if status_filter != "all" and status_filter not in INBOX_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status filter")

    applications = await Application.find_all().to_list()
    counts = Counter(app.status for app in applications)
    counts_payload = InboxCounts(
        **{status_name: counts.get(status_name, 0) for status_name in INBOX_STATUSES}
    )

    if status_filter != "all":
        applications = [app for app in applications if app.status == status_filter]

    items: List[InboxItem] = []
    for app in applications:
        job = await Job.get(app.job_id)
        user = await User.get(app.user_id)
        items.append(
            InboxItem(
                id=str(app.id),
                job_title=job.title if job else "Unknown job",
                candidate_email=user.email if user else None,
                status=app.status,
                updated_at=app.updated_at,
            )
        )

    return InboxResponse(counts=counts_payload, items=items)


@router.patch("/applications/{application_id}", response_model=InboxItem)
async def update_application_status(
    application_id: str,
    payload: StatusUpdateRequest,
    current_user: User = Depends(require_role("employer")),
):
    if payload.status not in INBOX_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")

    app = await Application.get(application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    app.status = payload.status
    app.updated_at = datetime.utcnow()
    await app.save()

    job = await Job.get(app.job_id)
    user = await User.get(app.user_id)

    return InboxItem(
        id=str(app.id),
        job_title=job.title if job else "Unknown job",
        candidate_email=user.email if user else None,
        status=app.status,
        updated_at=app.updated_at,
    )
