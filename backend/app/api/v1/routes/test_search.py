"""
Simplified test search endpoint to verify basic functionality
"""
from fastapi import APIRouter, Query
from typing import List, Optional
from app.models.job import Job, JobStatus, JobResponse, WorkType

router = APIRouter()

@router.get("/test-search")
async def test_search(
    remote_only: bool = Query(False),
    limit: int = Query(10)
):
    """Simple test search endpoint"""
    query = {"status": JobStatus.ACTIVE}
    
    if remote_only:
        query["work_type"] = WorkType.REMOTE
    
    jobs = await Job.find(query).limit(limit).to_list()
    
    return {
        "count": len(jobs),
        "jobs": [{"id": str(job.id), "title": job.title, "work_type": job.work_type} for job in jobs]
    }

