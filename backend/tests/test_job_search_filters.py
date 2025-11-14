"""
Tests for the advanced job search and filter endpoints.

Tests ST-018: Advanced Job Search & Filters
"""
import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient

from app.models.job import Job, WorkType, JobType, ExperienceLevel, CompanySize, JobStatus


@pytest.mark.asyncio
async def test_search_by_keywords(client: AsyncClient):
    """Test keyword search in title and description."""
    # Create test jobs
    job1 = Job(
        title="Senior Python Developer",
        description="We need a Python expert",
        skills=["Python", "Django"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    job2 = Job(
        title="JavaScript Engineer",
        description="Looking for JS skills",
        skills=["JavaScript", "React"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await job1.insert()
    await job2.insert()
    
    # Search for Python
    response = await client.get("/api/v1/jobs/search?q=Python")
    assert response.status_code == 200
    data = response.json()
    
    assert data["pagination"]["total_results"] >= 1
    titles = [job["title"] for job in data["jobs"]]
    assert any("Python" in title for title in titles)
    
    # Cleanup
    await job1.delete()
    await job2.delete()


@pytest.mark.asyncio
async def test_search_remote_only(client: AsyncClient):
    """Test filtering for remote jobs only."""
    # Create test jobs
    remote_job = Job(
        title="Remote Software Engineer",
        description="100% remote position",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    onsite_job = Job(
        title="Onsite Developer",
        description="Office position",
        skills=["Java"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await remote_job.insert()
    await onsite_job.insert()
    
    # Filter for remote only
    response = await client.get("/api/v1/jobs/search?remote_only=true")
    assert response.status_code == 200
    data = response.json()
    
    # All results should be remote
    for job in data["jobs"]:
        assert job["work_type"] == "remote"
    
    # Cleanup
    await remote_job.delete()
    await onsite_job.delete()


@pytest.mark.asyncio
async def test_search_salary_range(client: AsyncClient):
    """Test filtering by salary range."""
    # Create jobs with different salaries
    high_salary_job = Job(
        title="Senior Engineer",
        description="High paying role",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        salary_min=150000,
        salary_max=200000,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    low_salary_job = Job(
        title="Junior Developer",
        description="Entry level position",
        skills=["Python"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.ENTRY,
        salary_min=60000,
        salary_max=80000,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await high_salary_job.insert()
    await low_salary_job.insert()
    
    # Filter for high salaries (min 100k)
    response = await client.get("/api/v1/jobs/search?salary_min=100000")
    assert response.status_code == 200
    data = response.json()
    
    # All results should have salary_max >= 100k
    for job in data["jobs"]:
        if job["salary_max"]:
            assert job["salary_max"] >= 100000
    
    # Cleanup
    await high_salary_job.delete()
    await low_salary_job.delete()


@pytest.mark.asyncio
async def test_search_posted_within(client: AsyncClient):
    """Test filtering by posting date."""
    # Create jobs posted at different times
    recent_job = Job(
        title="New Job",
        description="Posted today",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    old_job = Job(
        title="Old Job",
        description="Posted 40 days ago",
        skills=["Java"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow() - timedelta(days=40),
    )
    await recent_job.insert()
    await old_job.insert()
    
    # Filter for last 7 days
    response = await client.get("/api/v1/jobs/search?posted_within=7d")
    assert response.status_code == 200
    data = response.json()
    
    # Check that recent job is in results
    job_ids = [job["id"] for job in data["jobs"]]
    assert str(recent_job.id) in job_ids
    assert str(old_job.id) not in job_ids
    
    # Cleanup
    await recent_job.delete()
    await old_job.delete()


@pytest.mark.asyncio
async def test_search_experience_level(client: AsyncClient):
    """Test filtering by experience level."""
    # Create jobs at different levels
    senior_job = Job(
        title="Senior Engineer",
        description="Senior position",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    entry_job = Job(
        title="Junior Developer",
        description="Entry level",
        skills=["Python"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.ENTRY,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await senior_job.insert()
    await entry_job.insert()
    
    # Filter for senior level
    response = await client.get("/api/v1/jobs/search?experience_levels=senior")
    assert response.status_code == 200
    data = response.json()
    
    # All results should be senior level
    for job in data["jobs"]:
        assert job["experience_level"] == "senior"
    
    # Cleanup
    await senior_job.delete()
    await entry_job.delete()


@pytest.mark.asyncio
async def test_search_easy_apply(client: AsyncClient):
    """Test filtering for Easy Apply jobs."""
    easy_job = Job(
        title="Easy Apply Job",
        description="Quick application",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        easy_apply=True,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    regular_job = Job(
        title="Regular Job",
        description="Standard application",
        skills=["Java"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        easy_apply=False,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await easy_job.insert()
    await regular_job.insert()
    
    # Filter for Easy Apply
    response = await client.get("/api/v1/jobs/search?easy_apply=true")
    assert response.status_code == 200
    data = response.json()
    
    # All results should have easy_apply=True
    for job in data["jobs"]:
        assert job["easy_apply"] is True
    
    # Cleanup
    await easy_job.delete()
    await regular_job.delete()


@pytest.mark.asyncio
async def test_search_multiple_filters(client: AsyncClient):
    """Test combining multiple filters."""
    # Create a job matching all criteria
    matching_job = Job(
        title="Senior Python Developer",
        description="Remote position with great salary",
        skills=["Python", "AWS"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        salary_min=120000,
        salary_max=160000,
        easy_apply=True,
        company_rating=4.5,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    
    # Create a job that doesn't match
    non_matching_job = Job(
        title="Junior Java Developer",
        description="Onsite entry level",
        skills=["Java"],
        work_type=WorkType.ONSITE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.ENTRY,
        salary_min=60000,
        salary_max=80000,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    
    await matching_job.insert()
    await non_matching_job.insert()
    
    # Apply multiple filters
    response = await client.get(
        "/api/v1/jobs/search?"
        "remote_only=true&"
        "experience_levels=senior&"
        "salary_min=100000&"
        "easy_apply=true"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should find the matching job
    job_ids = [job["id"] for job in data["jobs"]]
    assert str(matching_job.id) in job_ids
    assert str(non_matching_job.id) not in job_ids
    
    # Cleanup
    await matching_job.delete()
    await non_matching_job.delete()


@pytest.mark.asyncio
async def test_search_pagination(client: AsyncClient):
    """Test pagination in search results."""
    # Create multiple jobs
    jobs = []
    for i in range(25):
        job = Job(
            title=f"Job {i}",
            description=f"Description {i}",
            skills=["Python"],
            work_type=WorkType.REMOTE,
            job_type=JobType.FULL_TIME,
            experience_level=ExperienceLevel.MID,
            status=JobStatus.ACTIVE,
            posted_at=datetime.utcnow(),
        )
        await job.insert()
        jobs.append(job)
    
    # Get first page
    response = await client.get("/api/v1/jobs/search?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["jobs"]) <= 10
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["total_results"] >= 25
    assert data["pagination"]["has_more"] is True
    
    # Get second page
    response = await client.get("/api/v1/jobs/search?page=2&page_size=10")
    assert response.status_code == 200
    data = response.json()
    
    assert data["pagination"]["page"] == 2
    
    # Cleanup
    for job in jobs:
        await job.delete()


@pytest.mark.asyncio
async def test_get_filter_options(client: AsyncClient):
    """Test the filter options endpoint."""
    # Create jobs with various attributes
    job1 = Job(
        title="Remote Python Job",
        description="Test",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.SENIOR,
        city="San Francisco",
        state="CA",
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    job2 = Job(
        title="Onsite Java Job",
        description="Test",
        skills=["Java"],
        work_type=WorkType.ONSITE,
        job_type=JobType.CONTRACT,
        experience_level=ExperienceLevel.MID,
        city="New York",
        state="NY",
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    await job1.insert()
    await job2.insert()
    
    # Get filter options
    response = await client.get("/api/v1/jobs/filter-options")
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "work_types" in data
    assert "job_types" in data
    assert "experience_levels" in data
    assert "cities" in data
    assert "salary_ranges" in data
    
    # Check that options have counts
    assert len(data["work_types"]) > 0
    for option in data["work_types"]:
        assert "value" in option
        assert "label" in option
        assert "count" in option
        assert option["count"] > 0
    
    # Cleanup
    await job1.delete()
    await job2.delete()


@pytest.mark.asyncio
async def test_search_ignores_archived_jobs(client: AsyncClient):
    """Test that archived jobs are not returned in search results."""
    active_job = Job(
        title="Active Job",
        description="This is active",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ACTIVE,
        posted_at=datetime.utcnow(),
    )
    archived_job = Job(
        title="Archived Job",
        description="This is archived",
        skills=["Python"],
        work_type=WorkType.REMOTE,
        job_type=JobType.FULL_TIME,
        experience_level=ExperienceLevel.MID,
        status=JobStatus.ARCHIVED,
        posted_at=datetime.utcnow(),
    )
    await active_job.insert()
    await archived_job.insert()
    
    # Search without filters
    response = await client.get("/api/v1/jobs/search")
    assert response.status_code == 200
    data = response.json()
    
    # Should only return active jobs
    job_ids = [job["id"] for job in data["jobs"]]
    assert str(active_job.id) in job_ids
    assert str(archived_job.id) not in job_ids
    
    # Cleanup
    await active_job.delete()
    await archived_job.delete()

