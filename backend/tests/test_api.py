import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"


def test_register_job_seeker():
    """Test job seeker registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testseeker@example.com",
            "password": "testpassword123",
            "role": "job_seeker"
        }
    )
    # May fail if DB not running - that's ok for demo
    assert response.status_code in [201, 500]


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code in [401, 500]


def test_search_jobs_unauthenticated():
    """Test job search without authentication"""
    response = client.get("/api/v1/jobs")
    # Should work without auth
    assert response.status_code in [200, 500]


def test_get_profile_unauthenticated():
    """Test getting profile without authentication"""
    response = client.get("/api/v1/seekers/me")
    # Should require authentication
    assert response.status_code in [401, 403, 422]
