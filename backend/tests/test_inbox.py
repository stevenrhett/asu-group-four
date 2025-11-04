import pytest

from app.models.application import Application
from app.models.job import Job

pytestmark = pytest.mark.asyncio


STATUSES = ["applied", "viewed", "shortlisted", "interview", "rejected"]


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


async def test_inbox_listing_and_updates(app_client):
    employer_email = "inbox-employer@test.com"
    seeker_email = "inbox-seeker@test.com"
    password = "SecurePass!123"

    await register(app_client, employer_email, password, "employer")
    employer_token = await login(app_client, employer_email, password)

    job_payload = {
        "title": "Backend Engineer",
        "description": "Work on APIs.",
        "location": "Remote",
        "skills": ["python", "fastapi"],
    }
    await create_job(app_client, employer_token, job_payload)
    job_doc = await Job.find_one(Job.title == job_payload["title"])
    assert job_doc is not None

    await register(app_client, seeker_email, password, "seeker")
    seeker_token = await login(app_client, seeker_email, password)
    application = await apply_for_job(app_client, seeker_token, str(job_doc.id))

    response = await app_client.get(
        "/api/v1/inbox/applications",
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["counts"]["applied"] == 1
    assert data["counts"]["shortlisted"] == 0
    assert data["items"], "Expected at least one inbox item"
    assert data["items"][0]["candidate_email"] == seeker_email

    response_filtered = await app_client.get(
        "/api/v1/inbox/applications",
        params={"status": "applied"},
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response_filtered.status_code == 200
    filtered = response_filtered.json()
    assert all(item["status"] == "applied" for item in filtered["items"])

    patch_response = await app_client.patch(
        f"/api/v1/inbox/applications/{application['id']}",
        json={"status": "shortlisted"},
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert patch_response.status_code == 200
    patched = patch_response.json()
    assert patched["status"] == "shortlisted"

    # Data in DB updated
    updated = await Application.get(application["id"])
    assert updated.status == "shortlisted"

    response_after = await app_client.get(
        "/api/v1/inbox/applications",
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert response_after.status_code == 200
    after_data = response_after.json()
    assert after_data["counts"]["shortlisted"] == 1
