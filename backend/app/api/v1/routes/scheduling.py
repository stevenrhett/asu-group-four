from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()


class ScheduleRequest(BaseModel):
    title: str
    start_iso: str
    end_iso: str
    location: Optional[str] = None
    attendees: List[EmailStr]


def _generate_ics(req: ScheduleRequest) -> str:
    # Minimal placeholder ICS content; extend later with UID/DTSTAMP/timezones
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//ASU Group Four//Job Portal//EN\n"
        "BEGIN:VEVENT\n"
        f"SUMMARY:{req.title}\n"
        f"DTSTART:{req.start_iso}\n"
        f"DTEND:{req.end_iso}\n"
        f"LOCATION:{req.location or ''}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )


@router.post("/", status_code=201)
async def schedule_interview(req: ScheduleRequest):
    ics = _generate_ics(req)
    # TODO: send email with ICS attached
    return {"status": "scheduled", "ics": ics}


@router.put("/{schedule_id}")
async def reschedule_interview(schedule_id: str, req: ScheduleRequest):
    ics = _generate_ics(req)
    # TODO: send update email with new ICS
    return {"status": "rescheduled", "id": schedule_id, "ics": ics}


@router.delete("/{schedule_id}")
async def cancel_interview(schedule_id: str):
    # TODO: send cancellation email
    return {"status": "canceled", "id": schedule_id}

