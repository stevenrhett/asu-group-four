"""
Test suite for ST-016: Account Settings & Profile Management

Tests cover:
- User profile retrieval with contact info
- Contact information updates
- Account deactivation (soft delete)
- Permanent account deletion with GDPR compliance
- Resume re-upload for seekers
- Role-based access control
"""

from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.models.application import Application
from app.models.job import Job
from app.models.profile import Profile
from app.models.user import User
from app.models.event import EventLog


@pytest.mark.asyncio
async def test_get_current_user_profile(app_client: AsyncClient):
    """AC-1: User can view their email, contact info, and account age"""
    # Create user with contact info
    user = User(
        email="testuser@example.com",
        hashed_password="hashed",
        role="seeker",
        phone="+1234567890",
        linkedin_url="https://linkedin.com/in/testuser",
        website_url="https://testuser.com",
        is_active=True,
        created_at=datetime(2024, 1, 1)
    )
    await user.insert()

    # Login
    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": ""},
    )
    token = response.json()["access_token"]

    # Get profile
    response = await app_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "seeker"
    assert data["phone"] == "+1234567890"
    assert data["linkedin_url"] == "https://linkedin.com/in/testuser"
    assert data["website_url"] == "https://testuser.com"
    assert data["is_active"] is True
    assert "created_at" in data


@pytest.mark.asyncio
async def test_update_contact_information(app_client: AsyncClient):
    """AC-2: User can update contact information"""
    # Create user
    user = User(
        email="testuser@example.com",
        hashed_password="hashed",
        role="seeker"
    )
    await user.insert()

    # Login
    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": ""},
    )
    token = response.json()["access_token"]

    # Update contact info
    response = await app_client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "phone": "+1987654321",
            "linkedin_url": "https://linkedin.com/in/updated",
            "website_url": "https://updated.com"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+1987654321"
    assert data["linkedin_url"] == "https://linkedin.com/in/updated"
    assert data["website_url"] == "https://updated.com"

    # Verify persistence
    updated_user = await User.get(user.id)
    assert updated_user.phone == "+1987654321"
    assert updated_user.linkedin_url == "https://linkedin.com/in/updated"
    assert updated_user.website_url == "https://updated.com"


@pytest.mark.asyncio
async def test_update_contact_info_partial(app_client: AsyncClient):
    """AC-2: Partial updates work correctly"""
    user = User(
        email="testuser@example.com",
        hashed_password="hashed",
        role="seeker",
        phone="+1111111111",
        linkedin_url="https://linkedin.com/in/original"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": ""},
    )
    token = response.json()["access_token"]

    # Update only phone
    response = await app_client.patch(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": "+1222222222"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+1222222222"
    # LinkedIn URL should remain unchanged
    assert data["linkedin_url"] == "https://linkedin.com/in/original"


@pytest.mark.asyncio
async def test_deactivate_account(app_client: AsyncClient):
    """AC-3: User can deactivate account (soft delete)"""
    user = User(
        email="testuser@example.com",
        hashed_password="hashed",
        role="seeker",
        is_active=True
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": ""},
    )
    token = response.json()["access_token"]

    # Deactivate account
    response = await app_client.post(
        "/api/v1/users/me/deactivate",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "deactivated" in response.json()["message"].lower()

    # Verify user is_active is False
    deactivated_user = await User.get(user.id)
    assert deactivated_user.is_active is False

    # Verify audit log event was created
    events = await EventLog.find(EventLog.event_type == "account_deactivated").to_list()
    assert len(events) == 1
    assert events[0].user_id == str(user.id)


@pytest.mark.asyncio
async def test_delete_account_permanently_with_password(app_client: AsyncClient):
    """AC-4: User can permanently delete account with password confirmation"""
    from app.core.security import hash_password

    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("mypassword"),
        role="seeker"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "mypassword"},
    )
    token = response.json()["access_token"]

    # Delete with password
    response = await app_client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "mypassword"}
    )

    assert response.status_code == 200
    assert "permanently deleted" in response.json()["message"].lower()

    # Verify user is deleted
    deleted_user = await User.get(user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_account_invalid_password(app_client: AsyncClient):
    """AC-4: Permanent deletion requires correct password"""
    from app.core.security import hash_password

    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("correctpassword"),
        role="seeker"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "correctpassword"},
    )
    token = response.json()["access_token"]

    # Try to delete with wrong password
    response = await app_client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert "invalid password" in response.json()["detail"].lower()

    # Verify user still exists
    existing_user = await User.get(user.id)
    assert existing_user is not None


@pytest.mark.asyncio
async def test_gdpr_deletion_anonymizes_applications(app_client: AsyncClient):
    """AC-4: GDPR deletion anonymizes user's applications"""
    from app.core.security import hash_password

    # Create user
    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password"),
        role="seeker"
    )
    await user.insert()

    # Create job
    job = Job(
        title="Test Job",
        description="Test",
        employer_id="employer123",
        status="active"
    )
    await job.insert()

    # Create application
    application = Application(
        job_id=str(job.id),
        user_id=str(user.id),
        status="applied"
    )
    await application.insert()

    # Login and delete
    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    token = response.json()["access_token"]

    response = await app_client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "password"}
    )

    assert response.status_code == 200

    # Verify application is anonymized
    anonymized_app = await Application.get(application.id)
    assert anonymized_app.user_id == "deleted_user"


@pytest.mark.asyncio
async def test_gdpr_deletion_deletes_profile_and_resume(app_client: AsyncClient):
    """AC-4: GDPR deletion removes profile and resume files"""
    from app.core.security import hash_password

    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password"),
        role="seeker"
    )
    await user.insert()

    # Create profile with mock resume path
    profile = Profile(
        user_id=str(user.id),
        skills=["Python", "FastAPI"],
        resume_path="/tmp/test_resume.pdf"
    )
    await profile.insert()

    # Mock file deletion
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.unlink") as mock_unlink:
        
        response = await app_client.post(
            "/api/v1/auth/login",
            data={"username": "testuser@example.com", "password": "password"},
        )
        token = response.json()["access_token"]

        response = await app_client.delete(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"password": "password"}
        )

        assert response.status_code == 200
        # Verify file deletion was called
        mock_unlink.assert_called_once()

    # Verify profile is deleted
    deleted_profile = await Profile.find_one(Profile.user_id == str(user.id))
    assert deleted_profile is None


@pytest.mark.asyncio
async def test_gdpr_deletion_creates_audit_log(app_client: AsyncClient):
    """AC-4: GDPR deletion logs event for compliance audit"""
    from app.core.security import hash_password

    user = User(
        email="testuser@example.com",
        hashed_password=hash_password("password"),
        role="seeker"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    token = response.json()["access_token"]

    response = await app_client.delete(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "password"}
    )

    assert response.status_code == 200

    # Verify audit log entry
    events = await EventLog.find(EventLog.event_type == "account_deleted_permanently").to_list()
    assert len(events) == 1
    event = events[0]
    assert event.user_id == str(user.id)
    assert event.metadata["email"] == "testuser@example.com"
    assert event.metadata["role"] == "seeker"


@pytest.mark.asyncio
async def test_resume_reupload_for_seekers(app_client: AsyncClient):
    """AC-5: Seekers can re-upload resume (reusing existing endpoint)"""
    from app.core.security import hash_password

    user = User(
        email="seeker@example.com",
        hashed_password=hash_password("password"),
        role="seeker"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "seeker@example.com", "password": "password"},
    )
    token = response.json()["access_token"]

    # Test that endpoint exists (actual upload tested in test_resume_upload.py)
    response = await app_client.post(
        "/api/v1/uploads/resume",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.pdf", b"fake pdf content", "application/pdf")}
    )

    # Will fail parsing but endpoint should be accessible
    assert response.status_code in [200, 400]  # 400 if parsing fails, which is expected


@pytest.mark.asyncio
async def test_employer_cannot_upload_resume(app_client: AsyncClient):
    """AC-5: Employers cannot access resume upload endpoint"""
    from app.core.security import hash_password

    user = User(
        email="employer@example.com",
        hashed_password=hash_password("password"),
        role="employer"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "employer@example.com", "password": "password"},
    )
    token = response.json()["access_token"]

    response = await app_client.post(
        "/api/v1/uploads/resume",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("resume.pdf", b"fake pdf content", "application/pdf")}
    )

    assert response.status_code == 403  # Forbidden for employers


@pytest.mark.asyncio
async def test_employer_views_settings(app_client: AsyncClient):
    """AC-6: Employers can access settings page (basic verification)"""
    from app.core.security import hash_password

    user = User(
        email="employer@example.com",
        hashed_password=hash_password("password"),
        role="employer"
    )
    await user.insert()

    response = await app_client.post(
        "/api/v1/auth/login",
        data={"username": "employer@example.com", "password": "password"},
    )
    token = response.json()["access_token"]

    # Get profile as employer
    response = await app_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "employer"


@pytest.mark.asyncio
async def test_unauthorized_access_to_settings(app_client: AsyncClient):
    """Ensure endpoints require authentication"""
    # Try to access without token
    response = await app_client.get("/api/v1/users/me")
    assert response.status_code == 401

    response = await app_client.patch("/api/v1/users/me", json={})
    assert response.status_code == 401

    response = await app_client.post("/api/v1/users/me/deactivate")
    assert response.status_code == 401

    response = await app_client.delete("/api/v1/users/me", json={"password": "test"})
    assert response.status_code == 401



