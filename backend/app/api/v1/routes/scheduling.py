from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.api.deps import require_role
from app.models.user import User
from app.services.email import EmailAttachment, EmailMessage, send_email
from app.services.ics import generate_ics

router = APIRouter()


class ScheduleRequest(BaseModel):
    title: str
    start_iso: str
    end_iso: str
    location: Optional[str] = None
    attendees: List[EmailStr]


SCHEDULE_SUBJECT = {
    "scheduled": "Interview scheduled",
    "rescheduled": "Interview rescheduled",
    "canceled": "Interview canceled",
}

SCHEDULE_BODY = {
    "scheduled": "Interview scheduled for {title}.\nStart: {start}\nEnd: {end}\nLocation: {location}",
    "rescheduled": "Interview rescheduled for {title}.\nNew start: {start}\nNew end: {end}\nLocation: {location}",
    "canceled": "Interview canceled for {title}.",
}


def _dispatch_schedule_email(
    action: str,
    req: ScheduleRequest,
    ics_content: str,
    employer_email: str,
) -> None:
    subject = SCHEDULE_SUBJECT[action]
    body_template = SCHEDULE_BODY[action]
    body = body_template.format(title=req.title, start=req.start_iso, end=req.end_iso, location=req.location or "TBD")
    attachment = EmailAttachment(filename="interview.ics", content=ics_content, mimetype="text/calendar")
    recipients = list({*req.attendees, employer_email})
    send_email(EmailMessage(to=recipients, subject=subject, body=body, attachments=[attachment]))


@router.post("/", status_code=201)
async def schedule_interview(req: ScheduleRequest, current_user: User = Depends(require_role("employer"))):
    ics = generate_ics(req.title, req.start_iso, req.end_iso, req.location)
    _dispatch_schedule_email("scheduled", req, ics, current_user.email)
    return {"status": "scheduled", "ics": ics}


@router.put("/{schedule_id}")
async def reschedule_interview(schedule_id: str, req: ScheduleRequest, current_user: User = Depends(require_role("employer"))):
    ics = generate_ics(req.title, req.start_iso, req.end_iso, req.location)
    _dispatch_schedule_email("rescheduled", req, ics, current_user.email)
    return {"status": "rescheduled", "id": schedule_id, "ics": ics}


@router.delete("/{schedule_id}")
async def cancel_interview(schedule_id: str, req: ScheduleRequest, current_user: User = Depends(require_role("employer"))):
    ics = generate_ics(req.title, req.start_iso, req.end_iso, req.location, description="Interview canceled")
    _dispatch_schedule_email("canceled", req, ics, current_user.email)
    return {"status": "canceled", "id": schedule_id, "ics": ics}
