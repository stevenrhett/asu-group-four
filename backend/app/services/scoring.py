from __future__ import annotations

import math

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

import numpy as np
from app.models.job import Job
from app.services.normalization import tokenize


@dataclass
class RankedJob:
    job: Job
    score: float
    bm25_score: float
    vector_score: float
    explanations: List[dict]


def _compute_idf(jobs_tokens: Sequence[List[str]]) -> dict:
    num_docs = len(jobs_tokens)
    df = {}
    for tokens in jobs_tokens:
        unique_tokens = set(tokens)
        for token in unique_tokens:
            df[token] = df.get(token, 0) + 1
    idf = {}
    for token, freq in df.items():
        idf[token] = math.log(1 + (num_docs - freq + 0.5) / (freq + 0.5))
    return idf


def _bm25(
    query_tokens: List[str],
    jobs_tokens: Sequence[List[str]],
    idf: dict,
    k1: float = 1.6,
    b: float = 0.75,
) -> tuple[List[float], List[dict]]:
    avg_len = sum(len(tokens) for tokens in jobs_tokens) / max(len(jobs_tokens), 1)
    scores = []
    contributions: List[dict] = []
    for tokens in jobs_tokens:
        token_counts = {}
        for token in tokens:
            token_counts[token] = token_counts.get(token, 0) + 1
        doc_len = len(tokens)
        doc_score = 0.0
        token_contrib = {}
        for token in query_tokens:
            if token not in token_counts:
                continue
            tf = token_counts[token]
            denom = tf + k1 * (1 - b + b * doc_len / (avg_len or 1))
            contribution = idf.get(token, 0.0) * ((tf * (k1 + 1)) / denom)
            doc_score += contribution
            token_contrib[token] = contribution
        scores.append(doc_score)
        contributions.append(token_contrib)
    return scores, contributions


def _cosine_similarity(query_vector: List[float], job_vector: List[float]) -> float:
    if not query_vector or not job_vector:
        return 0.0
    q = np.array(query_vector, dtype=np.float32)
    j = np.array(job_vector, dtype=np.float32)
    norm_q = np.linalg.norm(q)
    norm_j = np.linalg.norm(j)
    if not norm_q or not norm_j:
        return 0.0
    return float(np.dot(q, j) / (norm_q * norm_j))


def build_query_tokens(skills: Iterable[str], titles: Iterable[str], extra_text: Optional[str] = None) -> List[str]:
    parts = list(skills) + list(titles)
    if extra_text:
        parts.append(extra_text)
    return tokenize(" ".join(parts))


def rank_jobs(
    jobs: Sequence[Job],
    query_tokens: List[str],
    query_vector: List[float],
    limit: int,
    bm25_weight: float,
    vector_weight: float,
    profile_skills: Optional[List[str]] = None,
    profile_titles: Optional[List[str]] = None,
) -> List[RankedJob]:
    if not jobs:
        return []

    weight_sum = bm25_weight + vector_weight
    if weight_sum == 0:
        bm25_weight = 1.0
        vector_weight = 0.0
        weight_sum = 1.0

    normalized_bm25_weight = bm25_weight / weight_sum
    normalized_vector_weight = vector_weight / weight_sum

    jobs_tokens = [job.tokens for job in jobs]
    idf = _compute_idf(jobs_tokens)
    bm25_scores, bm25_contributions = _bm25(query_tokens, jobs_tokens, idf)

    results: List[RankedJob] = []
    normalized_skills = profile_skills or []
    normalized_titles = [title.lower() for title in (profile_titles or [])]

    for job, bm25_score, token_contrib in zip(jobs, bm25_scores, bm25_contributions):
        if job.embedding:
            vector_score = _cosine_similarity(query_vector, job.embedding)
        else:
            vector_score = 0.0

        final_score = (normalized_bm25_weight * bm25_score) + (normalized_vector_weight * vector_score)
        explanations = []
        if normalized_skills:
            skill_matches = [skill for skill in job.skills if skill in normalized_skills]
            for skill in skill_matches:
                explanations.append({"label": skill, "weight": 1.0, "source": "skill"})
        if normalized_titles:
            job_title_lower = (job.title or "").lower()
            for title in normalized_titles:
                if title and title in job_title_lower:
                    explanations.append({"label": title, "weight": 0.8, "source": "title"})
        token_items = sorted(token_contrib.items(), key=lambda item: item[1], reverse=True)
        for token, weight in token_items[:5]:
            explanations.append({"label": token, "weight": float(weight), "source": "token"})
        if vector_score:
            explanations.append({"label": "Semantic match", "weight": vector_score, "source": "vector"})

        results.append(
            RankedJob(
                job=job,
                score=final_score,
                bm25_score=bm25_score,
                vector_score=vector_score,
                explanations=explanations,
            )
        )

    results.sort(key=lambda item: item.score, reverse=True)
    return results[:limit]
