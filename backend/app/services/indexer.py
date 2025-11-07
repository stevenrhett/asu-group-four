from datetime import datetime
from typing import Iterable, List, Optional

from app.models.job import Job
from app.services.embedding import embed_text
from app.services.normalization import (
    normalize_skills,
    normalize_text_chunks,
    normalize_title,
    tokenize,
)


def build_job_text(job: Job, normalized_skills: List[str]) -> str:
    parts: List[str] = [
        normalize_title(job.title),
        job.description.strip(),
        " ".join(normalized_skills),
    ]
    if job.location:
        parts.append(job.location)
    return normalize_text_chunks(*parts)


async def index_job(job: Job) -> Job:
    normalized_skills = normalize_skills(job.skills)
    normalized_text = build_job_text(job, normalized_skills)
    tokens = tokenize(normalized_text)
    vector = embed_text(normalized_text) if normalized_text else None

    job.skills = normalized_skills
    job.normalized_text = normalized_text
    job.tokens = tokens
    job.embedding = vector
    job.indexed_at = datetime.utcnow()
    await job.save()
    return job


async def index_jobs(jobs: Iterable[Job]) -> int:
    count = 0
    for job in jobs:
        await index_job(job)
        count += 1
    return count


def ensure_job_tokens(job: Job) -> bool:
    return bool(job.tokens and job.normalized_text)
