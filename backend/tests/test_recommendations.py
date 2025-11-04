import pytest

from app.models.profile import Profile
from app.models.user import User

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


async def reindex_jobs(client, token: str):
    response = await client.post(
        "/api/v1/recommendations/index",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


async def test_recommendations_flow(app_client):
    employer_email = "employer@test.com"
    seeker_email = "seeker@test.com"
    password = "SecurePass!123"

    await register(app_client, employer_email, password, "employer")
    employer_token = await login(app_client, employer_email, password)

    job_payload = {
        "title": "Senior Python Engineer",
        "description": "Work with FastAPI and MongoDB to build scalable services.",
        "location": "Remote",
        "skills": ["Python", "FastAPI", "MongoDB"],
    }
    await create_job(app_client, employer_token, job_payload)
    await reindex_jobs(app_client, employer_token)

    await register(app_client, seeker_email, password, "seeker")
    seeker_token = await login(app_client, seeker_email, password)

    user = await User.find_one(User.email == seeker_email)
    await Profile(
        user_id=str(user.id),
        skills=["python", "fastapi"],
        titles=["software engineer"],
        raw_text="Experienced Python engineer with FastAPI background.",
    ).insert()

    response = await app_client.get(
        "/api/v1/recommendations/",
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["results"], "Expected at least one recommendation"
    top_result = data["results"][0]
    assert "Senior Python Engineer" in top_result["title"]
    assert top_result["score"] >= 0
    assert top_result["bm25_score"] >= 0
    assert top_result["explanations"], "Explainability payload expected"
    labels = [item["label"] for item in top_result["explanations"]]
    assert any("python" in label for label in labels)


async def test_recommendations_with_query_only(app_client):
    employer_email = "employer2@test.com"
    password = "SecurePass!123"

    await register(app_client, employer_email, password, "employer")
    employer_token = await login(app_client, employer_email, password)

    job_payload = {
        "title": "Data Scientist",
        "description": "Machine learning role using Python and SQL.",
        "location": "Phoenix",
        "skills": ["python", "sql", "machine learning"],
    }
    await create_job(app_client, employer_token, job_payload)
    await reindex_jobs(app_client, employer_token)

    seeker_email = "queryonly@test.com"
    await register(app_client, seeker_email, password, "seeker")
    seeker_token = await login(app_client, seeker_email, password)

    response = await app_client.get(
        "/api/v1/recommendations/",
        params={"query": "machine learning python"},
        headers={"Authorization": f"Bearer {seeker_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["results"], "Expected recommendations using query text"
    assert any("Data Scientist" in rec["title"] for rec in data["results"])
    assert all("explanations" in rec for rec in data["results"])
