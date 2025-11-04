from typing import List, Optional

from pydantic import BaseModel


class RecommendationExplanation(BaseModel):
    label: str
    weight: float
    source: str


class Recommendation(BaseModel):
    job_id: str
    title: str
    location: Optional[str]
    score: float
    bm25_score: float
    vector_score: float
    skills: List[str]
    snippet: Optional[str]
    explanations: List[RecommendationExplanation]


class RecommendationResponse(BaseModel):
    results: List[Recommendation]
