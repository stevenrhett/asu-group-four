from typing import List, Optional
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


async def generate_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding for text using OpenAI"""
    if not client:
        logger.warning("OpenAI API key not configured")
        return None
    
    try:
        response = await client.embeddings.create(
            model=settings.OPENAI_EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        return None


async def generate_job_embedding(job_data: dict) -> Optional[List[float]]:
    """Generate embedding for job posting"""
    text = f"""
    Title: {job_data.get('title', '')}
    Description: {job_data.get('description', '')}
    Requirements: {', '.join(job_data.get('requirements', []))}
    Skills: {', '.join(job_data.get('skills_required', []))}
    Experience Level: {job_data.get('experience_level', '')}
    """
    return await generate_embedding(text.strip())


async def generate_profile_embedding(profile_data: dict) -> Optional[List[float]]:
    """Generate embedding for job seeker profile"""
    text = f"""
    Headline: {profile_data.get('headline', '')}
    Summary: {profile_data.get('summary', '')}
    Skills: {', '.join(profile_data.get('skills', []))}
    Experience: {profile_data.get('experience_text', '')}
    Education: {profile_data.get('education_text', '')}
    """
    return await generate_embedding(text.strip())


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
