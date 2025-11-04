from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from app.api.deps import require_role
from app.core.config import settings
from app.models.job import Job
from app.models.profile import Profile
from app.models.user import User
from app.schemas.recommendations import Recommendation, RecommendationResponse
from app.services.embedding import embed_text
from app.services.indexer import ensure_job_tokens, index_job, index_jobs
from app.services.normalization import normalize_text_chunks, tokenize
from app.services.scoring import build_query_tokens, rank_jobs

router = APIRouter()


class ReindexRequest(BaseModel):
    job_ids: Optional[List[str]] = None


@router.post("/index")
async def reindex_jobs(
    payload: Optional[ReindexRequest] = None,
    current_user: User = Depends(require_role("employer")),
):
    jobs: List[Job] = []
    if payload and payload.job_ids:
        for job_id in payload.job_ids:
            job = await Job.get(job_id)
            if job:
                jobs.append(job)
    else:
        jobs = await Job.find_all().to_list()
    if not jobs:
        return {"indexed": 0}
    indexed = await index_jobs(jobs)
    return {"indexed": indexed}


@router.get("/", response_model=RecommendationResponse)
async def get_recommendations(
    limit: int = Query(settings.recommendation_limit, ge=1, le=50),
    query: Optional[str] = None,
    current_user: User = Depends(require_role("seeker")),
):
    profile = await Profile.find_one(Profile.user_id == str(current_user.id))

    profile_skills = profile.skills if profile else []
    profile_titles = profile.titles if profile else []
    extra_text = query
    if profile and profile.raw_text:
        extra_text = normalize_text_chunks(profile.raw_text, extra_text or "")

    query_tokens = build_query_tokens(profile_skills, profile_titles, extra_text)

    if not query_tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile data or query provided for recommendations.",
        )

    query_text = normalize_text_chunks(" ".join(profile_skills), " ".join(profile_titles), extra_text or "")
    query_vector = embed_text(query_text) if query_text else []

    jobs = await Job.find_all().to_list()
    if not jobs:
        return RecommendationResponse(results=[])

    indexed_jobs: List[Job] = []
    for job in jobs:
        if not ensure_job_tokens(job):
            await index_job(job)
        if job.tokens:
            indexed_jobs.append(job)

    if not indexed_jobs:
        return RecommendationResponse(results=[])

    ranked = rank_jobs(
        indexed_jobs,
        query_tokens=query_tokens,
        query_vector=query_vector,
        limit=limit,
        bm25_weight=settings.scoring_bm25_weight,
        vector_weight=settings.scoring_vector_weight,
        profile_skills=profile_skills,
        profile_titles=profile_titles,
    )

    recommendations = [
        Recommendation(
            job_id=str(item.job.id),
            title=item.job.title,
            location=item.job.location,
            score=item.score,
            bm25_score=item.bm25_score,
            vector_score=item.vector_score,
            skills=item.job.skills,
            snippet=(item.job.description[:200] + "...") if item.job.description else None,
            explanations=[
                {
                    "label": explanation["label"],
                    "weight": explanation["weight"],
                    "source": explanation["source"],
                }
                for explanation in item.explanations
            ],
        )
        for item in ranked
    ]

    return RecommendationResponse(results=recommendations)
