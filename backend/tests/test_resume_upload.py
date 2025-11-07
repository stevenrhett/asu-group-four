from io import BytesIO
from pathlib import Path

import pytest
from docx import Document as DocxDocument

from app.core.config import settings
from app.models.profile import Profile
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def register(client, email: str, password: str, role: str):
    return await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "role": role},
    )


async def login(client, email: str, password: str):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def _build_resume_docx(content: str) -> bytes:
    document = DocxDocument()
    for line in content.splitlines():
        document.add_paragraph(line)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer.read()


async def test_resume_upload_creates_profile(app_client, tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "resume_storage_dir", str(tmp_path))

    email = "resume@example.com"
    password = "StrongPass!234"
    await register(app_client, email, password, "seeker")
    token = await login(app_client, email, password)

    resume_bytes = _build_resume_docx(
        "John Doe\nSoftware Engineer at Example\nSkills: Python, FastAPI, MongoDB"
    )

    response = await app_client.post(
        "/api/v1/uploads/resume",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "file": (
                "resume.docx",
                resume_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["user_id"] == str((await User.find_one(User.email == email)).id)
    assert "python" in payload["skills"]
    assert any("Software Engineer" in title for title in payload["titles"])

    profile = await Profile.find_one(Profile.user_id == payload["user_id"])
    assert profile is not None
    assert profile.skills == payload["skills"]
    saved_file = Path(profile.resume_path)
    assert saved_file.exists()
    assert saved_file.stat().st_size > 0


async def test_resume_upload_rejects_unsupported_type(app_client, tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "resume_storage_dir", str(tmp_path))
    email = "invalid-type@example.com"
    password = "StrongPass!123"
    await register(app_client, email, password, "seeker")
    token = await login(app_client, email, password)

    response = await app_client.post(
        "/api/v1/uploads/resume",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.exe", b"dummy", "application/octet-stream")},
    )
    assert response.status_code == 400
    assert "Unsupported resume format" in response.json()["detail"]
