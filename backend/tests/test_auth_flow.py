import pytest

from app.models.application import Application
from app.models.job import Job
from app.models.user import User


pytestmark = pytest.mark.asyncio


async def register(client, email: str, password: str, role: str):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "role": role},
    )
    return response


async def login(client, email: str, password: str):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response


async def test_register_and_login_flow(app_client):
    email = "seeker@example.com"
    password = "StrongPass123!"
    register_response = await register(app_client, email, password, "seeker")
    assert register_response.status_code == 201
    payload = register_response.json()
    assert payload["email"] == email
    assert payload["role"] == "seeker"

    user = await User.get(payload["id"])
    assert user is not None
    assert user.hashed_password != password  # password is hashed

    duplicate_response = await register(app_client, email, password, "seeker")
    assert duplicate_response.status_code == 400

    login_response = await login(app_client, email, password)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    invalid_login = await login(app_client, email, "WrongPass!")
    assert invalid_login.status_code == 401


async def test_role_protection_and_application_flow(app_client):
    # employer setup
    employer_email = "employer@example.com"
    employer_password = "EmployerPass!1"
    await register(app_client, employer_email, employer_password, "employer")
    employer_token = (await login(app_client, employer_email, employer_password)).json()["access_token"]

    # seeker setup
    seeker_email = "seeker2@example.com"
    seeker_password = "SeekPass!1"
    await register(app_client, seeker_email, seeker_password, "seeker")
    seeker_login_response = await login(app_client, seeker_email, seeker_password)
    seeker_token = seeker_login_response.json()["access_token"]

    # job creation requires employer role
    job_payload = {
        "title": "Data Scientist",
        "description": "Analyze data trends",
        "location": "Remote",
        "skills": ["python", "ml"],
    }
    unauthorized_job = await app_client.post("/api/v1/jobs/", json=job_payload)
    assert unauthorized_job.status_code == 401

    seeker_job_attempt = await app_client.post(
        "/api/v1/jobs/",
        json=job_payload,
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert seeker_job_attempt.status_code == 403

    employer_job_response = await app_client.post(
        "/api/v1/jobs/",
        json=job_payload,
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert employer_job_response.status_code == 201

    job = await Job.find_one(Job.title == "Data Scientist")
    assert job is not None

    # seeker applies to job
    application_response = await app_client.post(
        "/api/v1/applications/",
        json={"job_id": str(job.id)},
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert application_response.status_code == 201
    application_payload = application_response.json()
    application_id = application_payload["id"]

    application = await Application.get(application_id)
    assert application is not None
    assert application.user_id == str((await User.find_one(User.email == seeker_email)).id)

    # seeker can list their applications
    seeker_list = await app_client.get(
        "/api/v1/applications/",
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert seeker_list.status_code == 200
    seeker_data = seeker_list.json()
    assert len(seeker_data) == 1
    assert seeker_data[0]["id"] == application_id

    # employer sees all applications
    employer_list = await app_client.get(
        "/api/v1/applications/",
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert employer_list.status_code == 200
    employer_data = employer_list.json()
    assert len(employer_data) == 1

    # role enforcement on status update
    seeker_update_attempt = await app_client.patch(
        f"/api/v1/applications/{application_id}/status",
        json={"status": "interview"},
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert seeker_update_attempt.status_code == 403

    employer_update = await app_client.patch(
        f"/api/v1/applications/{application_id}/status",
        json={"status": "interview"},
        headers={"Authorization": f"Bearer {employer_token}"},
    )
    assert employer_update.status_code == 200
    assert employer_update.json()["status"] == "interview"

    # invalid token payload is rejected
    invalid_token_response = await app_client.post(
        "/api/v1/jobs/",
        json=job_payload,
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert invalid_token_response.status_code == 401
