import pytest

from app.models.application import Application
from app.models.job import Job
from app.models.user import User
from app.services.email import EMAIL_OUTBOX

pytestmark = pytest.mark.asyncio


async def register(client, email: str, password: str, role: str):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    response.raise_for_status()
    return response


async def login(client, email: str, password: str) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


async def create_job(client, token: str, payload: dict):
    response = await client.post(
        "/api/v1/jobs/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


async def apply_for_job(client, token: str, job_id: str):
    response = await client.post(
        "/api/v1/applications/",
        json={"job_id": job_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


async def test_status_update_sends_email(app_client):
    employer_email = "notify-employer@test.com"
    seeker_email = "notify-seeker@test.com"
    password = "SecurePass!123"

    await register(app_client, employer_email, password, "employer")
    employer_token = await login(app_client, employer_email, password)

    job_payload = {
        "title": "Data Analyst",
        "description": "Analyze data",
        "location": "Tempe",
        "skills": ["sql", "python"],
    }
    await create_job(app_client, employer_token, job_payload)
    job_doc = await Job.find_one(Job.title == job_payload["title"])

    await register(app_client, seeker_email, password, "seeker")
    seeker_token = await login(app_client, seeker_email, password)
    application = await apply_for_job(app_client, seeker_token, str(job_doc.id))

    response = await app_client.patch(
        f"/api/v1/applications/{application['id']}/status",
        json={"status": "shortlisted"},
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 200

    assert len(EMAIL_OUTBOX) == 2
    seeker_message = next(msg for msg in EMAIL_OUTBOX if seeker_email in msg.to)
    employer_message = next(msg for msg in EMAIL_OUTBOX if employer_email in msg.to)
    assert "shortlisted" in seeker_message.subject.lower()
    assert "shortlisted" in employer_message.subject.lower()


async def test_scheduling_emails_with_ics(app_client):
    employer_email = "schedule-employer@test.com"
    password = "SecurePass!123"

    await register(app_client, employer_email, password, "employer")
    employer_token = await login(app_client, employer_email, password)

    schedule_payload = {
        "title": "Interview with Candidate",
        "start_iso": "2025-11-04T15:00:00Z",
        "end_iso": "2025-11-04T16:00:00Z",
        "location": "Virtual",
        "attendees": ["candidate@test.com"],
    }

    response = await app_client.post(
        "/api/v1/scheduling/",
        json=schedule_payload,
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 201
    assert EMAIL_OUTBOX, "Expected email to be sent"
    schedule_email = EMAIL_OUTBOX[-1]
    assert schedule_email.attachments, "ICS attachment expected"
    assert schedule_email.attachments[0].content.startswith("BEGIN:VCALENDAR")

    reschedule_payload = {**schedule_payload, "start_iso": "2025-11-05T15:00:00Z"}
    response = await app_client.put(
        "/api/v1/scheduling/123",
        json=reschedule_payload,
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 200

    cancel_payload = {**schedule_payload}
    response = await app_client.request(
        "DELETE",
        "/api/v1/scheduling/123",
        json=cancel_payload,
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 200
