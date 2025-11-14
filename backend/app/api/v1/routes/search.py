"""
Job search and filter endpoints.

Provides comprehensive search functionality with advanced filters
for job seekers to find relevant opportunities.
"""
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.models.job import (
    Job,
    JobResponse,
    WorkType,
    JobType,
    ExperienceLevel,
    CompanySize,
    JobStatus
)
from app.api.v1.routes.jobs import job_to_response

router = APIRouter()


class JobSearchFilters(BaseModel):
    """Schema for job search filters."""
    # Keyword search
    q: Optional[str] = Field(None, description="Job title or keywords")
    location: Optional[str] = Field(None, description="City or location")
    radius: Optional[int] = Field(50, description="Search radius in miles", ge=0, le=500)
    
    # Toggle filters
    easy_apply: bool = Field(False, description="Easy Apply only")
    remote_only: bool = Field(False, description="Remote jobs only")
    
    # Salary filter
    salary_min: Optional[int] = Field(None, description="Minimum salary", ge=0)
    salary_max: Optional[int] = Field(None, description="Maximum salary", ge=0)
    hide_without_salary: bool = Field(False, description="Hide jobs without salary info")
    
    # Date posted filter
    posted_within: Optional[str] = Field(
        None,
        description="Filter by posting date",
        pattern="^(24h|7d|30d|any)$"
    )
    
    # Company filters
    min_rating: Optional[float] = Field(None, description="Minimum company rating", ge=1.0, le=5.0)
    company_sizes: Optional[List[CompanySize]] = Field(None, description="Filter by company size")
    companies: Optional[List[str]] = Field(None, description="Filter by company names")
    industries: Optional[List[str]] = Field(None, description="Filter by industries")
    
    # Job details
    work_types: Optional[List[WorkType]] = Field(None, description="Filter by work type")
    job_types: Optional[List[JobType]] = Field(None, description="Filter by job type")
    experience_levels: Optional[List[ExperienceLevel]] = Field(None, description="Filter by experience level")
    
    # Location
    cities: Optional[List[str]] = Field(None, description="Filter by cities")
    states: Optional[List[str]] = Field(None, description="Filter by states")
    
    # Skills
    skills: Optional[List[str]] = Field(None, description="Required skills")
    
    # Pagination
    page: int = Field(1, description="Page number", ge=1)
    page_size: int = Field(20, description="Results per page", ge=1, le=100)
    
    # Sort
    sort_by: str = Field("relevance", description="Sort order", pattern="^(relevance|newest|salary)$")


class PaginationResponse(BaseModel):
    """Pagination metadata."""
    page: int
    page_size: int
    total_results: int
    total_pages: int
    has_more: bool


class FilterCount(BaseModel):
    """Filter option with count."""
    value: str
    label: str
    count: int


class FilterOptionsResponse(BaseModel):
    """Available filter options with counts."""
    work_types: List[FilterCount]
    job_types: List[FilterCount]
    experience_levels: List[FilterCount]
    company_sizes: List[FilterCount]
    cities: List[FilterCount]
    states: List[FilterCount]
    salary_ranges: List[dict]


class JobSearchResponse(BaseModel):
    """Job search results with metadata."""
    jobs: List[JobResponse]
    pagination: PaginationResponse
    filters_applied: dict


@router.get("/search", response_model=JobSearchResponse)
async def search_jobs(
    # Keyword search
    q: Optional[str] = Query(None, description="Job title or keywords"),
    location: Optional[str] = Query(None, description="City or location"),
    radius: Optional[int] = Query(50, description="Search radius in miles", ge=0, le=500),
    
    # Toggle filters
    easy_apply: bool = Query(False, description="Easy Apply only"),
    remote_only: bool = Query(False, description="Remote jobs only"),
    
    # Salary filter
    salary_min: Optional[int] = Query(None, description="Minimum salary", ge=0),
    salary_max: Optional[int] = Query(None, description="Maximum salary", ge=0),
    hide_without_salary: bool = Query(False, description="Hide jobs without salary info"),
    
    # Date posted filter
    posted_within: Optional[str] = Query(None, description="Filter by posting date (24h, 7d, 30d, any)"),
    
    # Company filters
    min_rating: Optional[float] = Query(None, description="Minimum company rating", ge=1.0, le=5.0),
    company_sizes: Optional[str] = Query(None, description="Comma-separated company sizes"),
    companies: Optional[str] = Query(None, description="Comma-separated company names"),
    industries: Optional[str] = Query(None, description="Comma-separated industries"),
    
    # Job details
    work_types: Optional[str] = Query(None, description="Comma-separated work types"),
    job_types: Optional[str] = Query(None, description="Comma-separated job types"),
    experience_levels: Optional[str] = Query(None, description="Comma-separated experience levels"),
    
    # Location
    cities: Optional[str] = Query(None, description="Comma-separated cities"),
    states: Optional[str] = Query(None, description="Comma-separated states"),
    
    # Skills
    skills: Optional[str] = Query(None, description="Comma-separated required skills"),
    
    # Pagination
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(20, description="Results per page", ge=1, le=100),
    
    # Sort
    sort_by: str = Query("relevance", description="Sort order (relevance, newest, salary)"),
):
    """
    Advanced job search with comprehensive filters.
    
    Supports keyword search, location filtering, salary ranges, work types,
    experience levels, company ratings, and more.
    """
    # Build query
    query = {"status": JobStatus.ACTIVE}
    
    # Keyword search - search in title, description, and skills
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"skills": {"$in": [q]}}
        ]
    
    # Location search
    if location:
        location_query = {
            "$or": [
                {"location": {"$regex": location, "$options": "i"}},
                {"city": {"$regex": location, "$options": "i"}},
                {"state": {"$regex": location, "$options": "i"}}
            ]
        }
        # Merge with existing query
        if "$or" in query:
            query["$and"] = [{"$or": query["$or"]}, location_query]
            del query["$or"]
        else:
            query.update(location_query)
    
    # Easy apply filter
    if easy_apply:
        query["easy_apply"] = True
    
    # Remote filter
    if remote_only:
        query["work_type"] = WorkType.REMOTE
    elif work_types:
        work_types_list = [wt.strip() for wt in work_types.split(",")]
        query["work_type"] = {"$in": work_types_list}
    
    # Salary filter
    if hide_without_salary:
        query["salary_min"] = {"$ne": None}
    elif salary_min is not None or salary_max is not None:
        salary_conditions = []
        if salary_min is not None:
            # Job's max salary should be >= our minimum
            salary_conditions.append({"salary_max": {"$gte": salary_min}})
        if salary_max is not None:
            # Job's min salary should be <= our maximum
            salary_conditions.append({"salary_min": {"$lte": salary_max}})
        
        if salary_conditions:
            if "$and" in query:
                query["$and"].extend(salary_conditions)
            else:
                query["$and"] = salary_conditions
    
    # Date posted filter
    if posted_within and posted_within != "any":
        hours_map = {"24h": 24, "7d": 168, "30d": 720}
        hours = hours_map.get(posted_within, 720)
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        query["posted_at"] = {"$gte": cutoff}
    
    # Company rating
    if min_rating:
        query["company_rating"] = {"$gte": min_rating}
    
    # Experience level
    if experience_levels:
        exp_levels_list = [el.strip() for el in experience_levels.split(",")]
        query["experience_level"] = {"$in": exp_levels_list}
    
    # Job types
    if job_types:
        job_types_list = [jt.strip() for jt in job_types.split(",")]
        query["job_type"] = {"$in": job_types_list}
    
    # Cities
    if cities:
        cities_list = [c.strip() for c in cities.split(",")]
        query["city"] = {"$in": cities_list}
    
    # States
    if states:
        states_list = [s.strip() for s in states.split(",")]
        query["state"] = {"$in": states_list}
    
    # Companies
    if companies:
        companies_list = [c.strip() for c in companies.split(",")]
        query["company_name"] = {"$in": companies_list}
    
    # Company sizes
    if company_sizes:
        sizes_list = [cs.strip() for cs in company_sizes.split(",")]
        query["company_size"] = {"$in": sizes_list}
    
    # Industries
    if industries:
        industries_list = [i.strip() for i in industries.split(",")]
        query["industry"] = {"$in": industries_list}
    
    # Skills
    if skills:
        skills_list = [s.strip() for s in skills.split(",")]
        query["skills"] = {"$all": skills_list}
    
    # Calculate pagination
    skip = (page - 1) * page_size
    
    # Sorting
    sort_options = {
        "relevance": [("posted_at", -1)],  # Default: newest first
        "newest": [("posted_at", -1)],
        "salary": [("salary_max", -1), ("salary_min", -1)]
    }
    sort = sort_options.get(sort_by, [("posted_at", -1)])
    
    # Execute query
    total_count = await Job.find(query).count()
    jobs = await Job.find(query).sort(sort).skip(skip).limit(page_size).to_list()
    
    # Calculate pagination metadata
    total_pages = (total_count + page_size - 1) // page_size
    has_more = page < total_pages
    
    # Build filters_applied summary
    filters_applied = {}
    if q:
        filters_applied["keywords"] = q
    if location:
        filters_applied["location"] = location
    if easy_apply:
        filters_applied["easy_apply"] = True
    if remote_only:
        filters_applied["remote_only"] = True
    if salary_min or salary_max:
        filters_applied["salary_range"] = f"${salary_min or 0:,} - ${salary_max or 0:,}"
    if posted_within:
        filters_applied["posted_within"] = posted_within
    if min_rating:
        filters_applied["min_rating"] = min_rating
    
    return JobSearchResponse(
        jobs=[job_to_response(job) for job in jobs],
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            total_results=total_count,
            total_pages=total_pages,
            has_more=has_more
        ),
        filters_applied=filters_applied
    )


@router.get("/filter-options", response_model=FilterOptionsResponse)
async def get_filter_options():
    """
    Get available filter options with counts.
    
    Returns counts for each filter option to help users see
    how many jobs match each filter.
    """
    # Get counts for each filter type using aggregation
    active_jobs_query = {"status": JobStatus.ACTIVE}
    
    # Work types
    work_types_agg = await Job.aggregate([
        {"$match": active_jobs_query},
        {"$group": {"_id": "$work_type", "count": {"$sum": 1}}}
    ]).to_list()
    
    work_types_map = {
        "remote": "Remote",
        "hybrid": "Hybrid",
        "onsite": "On-site"
    }
    work_types = [
        FilterCount(
            value=wt["_id"],
            label=work_types_map.get(wt["_id"], wt["_id"]),
            count=wt["count"]
        )
        for wt in work_types_agg if wt["_id"]
    ]
    
    # Job types
    job_types_agg = await Job.aggregate([
        {"$match": active_jobs_query},
        {"$group": {"_id": "$job_type", "count": {"$sum": 1}}}
    ]).to_list()
    
    job_types_map = {
        "full_time": "Full-time",
        "part_time": "Part-time",
        "contract": "Contract",
        "internship": "Internship"
    }
    job_types = [
        FilterCount(
            value=jt["_id"],
            label=job_types_map.get(jt["_id"], jt["_id"]),
            count=jt["count"]
        )
        for jt in job_types_agg if jt["_id"]
    ]
    
    # Experience levels
    exp_levels_agg = await Job.aggregate([
        {"$match": active_jobs_query},
        {"$group": {"_id": "$experience_level", "count": {"$sum": 1}}}
    ]).to_list()
    
    exp_levels_map = {
        "entry": "Entry Level",
        "mid": "Mid-Level",
        "senior": "Senior",
        "lead": "Lead/Principal"
    }
    experience_levels = [
        FilterCount(
            value=el["_id"],
            label=exp_levels_map.get(el["_id"], el["_id"]),
            count=el["count"]
        )
        for el in exp_levels_agg if el["_id"]
    ]
    
    # Company sizes
    company_sizes_agg = await Job.aggregate([
        {"$match": active_jobs_query},
        {"$group": {"_id": "$company_size", "count": {"$sum": 1}}}
    ]).to_list()
    
    company_sizes_map = {
        "startup": "Startup (1-50)",
        "small": "Small (51-200)",
        "medium": "Medium (201-1000)",
        "large": "Large (1001-10000)",
        "enterprise": "Enterprise (10000+)"
    }
    company_sizes = [
        FilterCount(
            value=cs["_id"],
            label=company_sizes_map.get(cs["_id"], cs["_id"]),
            count=cs["count"]
        )
        for cs in company_sizes_agg if cs["_id"]
    ]
    
    # Cities (top 20)
    cities_agg = await Job.aggregate([
        {"$match": {**active_jobs_query, "city": {"$ne": None}}},
        {"$group": {"_id": "$city", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]).to_list()
    
    cities = [
        FilterCount(value=c["_id"], label=c["_id"], count=c["count"])
        for c in cities_agg
    ]
    
    # States (all)
    states_agg = await Job.aggregate([
        {"$match": {**active_jobs_query, "state": {"$ne": None}}},
        {"$group": {"_id": "$state", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]).to_list()
    
    states = [
        FilterCount(value=s["_id"], label=s["_id"], count=s["count"])
        for s in states_agg
    ]
    
    # Salary ranges
    salary_ranges = [
        {"min": 0, "max": 75000, "label": "$0-$75k"},
        {"min": 75000, "max": 100000, "label": "$75k-$100k"},
        {"min": 100000, "max": 150000, "label": "$100k-$150k"},
        {"min": 150000, "max": 200000, "label": "$150k-$200k"},
        {"min": 200000, "max": None, "label": "$200k+"}
    ]
    
    return FilterOptionsResponse(
        work_types=work_types,
        job_types=job_types,
        experience_levels=experience_levels,
        company_sizes=company_sizes,
        cities=cities,
        states=states,
        salary_ranges=salary_ranges
    )

