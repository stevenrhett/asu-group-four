from typing import List, Dict
from app.ai.embeddings import cosine_similarity
from app.core.logging import get_logger

logger = get_logger(__name__)


def jaccard_similarity(set1: List[str], set2: List[str]) -> float:
    """Calculate Jaccard similarity between two sets"""
    if not set1 or not set2:
        return 0.0
    
    s1 = set([s.lower() for s in set1])
    s2 = set([s.lower() for s in set2])
    
    intersection = len(s1 & s2)
    union = len(s1 | s2)
    
    return intersection / union if union > 0 else 0.0


def match_experience_level(seeker_experience: str, job_level: str) -> float:
    """Match experience levels"""
    levels = ["entry", "mid", "senior", "lead", "executive"]
    
    try:
        seeker_idx = levels.index(seeker_experience.lower())
        job_idx = levels.index(job_level.lower())
        
        # Perfect match
        if seeker_idx == job_idx:
            return 1.0
        # Close match (±1 level)
        elif abs(seeker_idx - job_idx) == 1:
            return 0.7
        # Acceptable match (±2 levels)
        elif abs(seeker_idx - job_idx) == 2:
            return 0.4
        else:
            return 0.1
    except ValueError:
        return 0.5  # Default if levels not found


def match_location(seeker_preferences: dict, job_location: dict) -> float:
    """Match location preferences"""
    # Remote job - always a good match
    if job_location.get("is_remote", False):
        return 1.0
    
    # Check if seeker willing to relocate
    if seeker_preferences.get("willing_to_relocate", False):
        return 0.8
    
    # Check preferred locations
    preferred_locs = seeker_preferences.get("preferred_locations", [])
    job_city = job_location.get("city", "").lower()
    
    for loc in preferred_locs:
        if loc.lower() in job_city or job_city in loc.lower():
            return 1.0
    
    return 0.3  # Low match if location doesn't align


def calculate_match_score(
    job_data: dict,
    profile_data: dict,
    job_embedding: List[float] = None,
    profile_embedding: List[float] = None
) -> Dict[str, float]:
    """
    Calculate comprehensive match score between job and profile
    
    Returns:
        dict with score and breakdown
    """
    
    # 1. Semantic Similarity (50%) - from embeddings
    semantic_score = 0.5
    if job_embedding and profile_embedding:
        semantic_score = cosine_similarity(job_embedding, profile_embedding)
    
    # 2. Skills Match (30%)
    job_skills = job_data.get("skills_required", [])
    profile_skills = profile_data.get("skills", [])
    skills_score = jaccard_similarity(job_skills, profile_skills)
    
    # 3. Experience Level Match (10%)
    experience_score = match_experience_level(
        profile_data.get("experience_level", "mid"),
        job_data.get("experience_level", "mid")
    )
    
    # 4. Location Match (10%)
    location_score = match_location(
        profile_data.get("preferences", {}),
        job_data.get("location", {})
    )
    
    # Weighted combination
    final_score = (
        semantic_score * 0.5 +
        skills_score * 0.3 +
        experience_score * 0.1 +
        location_score * 0.1
    ) * 100
    
    return {
        "total_score": round(final_score, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "skills_score": round(skills_score * 100, 2),
        "experience_score": round(experience_score * 100, 2),
        "location_score": round(location_score * 100, 2),
    }


def generate_match_explanation(scores: Dict[str, float]) -> str:
    """Generate human-readable explanation of match"""
    explanations = []
    
    if scores["semantic_score"] > 70:
        explanations.append("Strong alignment with job description and requirements")
    elif scores["semantic_score"] > 50:
        explanations.append("Moderate alignment with job description")
    
    if scores["skills_score"] > 60:
        explanations.append(f"Good skills match ({scores['skills_score']:.0f}%)")
    elif scores["skills_score"] > 30:
        explanations.append(f"Partial skills match ({scores['skills_score']:.0f}%)")
    
    if scores["experience_score"] > 80:
        explanations.append("Experience level perfectly matches requirements")
    elif scores["experience_score"] > 50:
        explanations.append("Experience level is close to requirements")
    
    if scores["location_score"] > 80:
        explanations.append("Location preferences align well")
    
    return ". ".join(explanations) if explanations else "Basic compatibility found"
