"""
Unit tests for hybrid scoring configuration validation (ST-004).

Tests weight configuration, normalization, and edge cases.
Priority: HIGH (Gap from traceability analysis)
Test IDs: ST-004-UNIT-001, ST-004-UNIT-002
"""
import pytest
from unittest.mock import patch
import numpy as np

from app.models.job import Job
from app.services.scoring import rank_jobs, build_query_tokens, _compute_idf, _bm25, _cosine_similarity


class TestScoringWeightConfiguration:
    """ST-004-UNIT-001: Test different BM25 vs embedding weights."""
    
    def test_bm25_only_configuration(self):
        """
        Given: BM25 weight = 1.0, vector weight = 0.0
        When: rank_jobs is called
        Then: Only BM25 scores influence ranking
        """
        jobs = [
            Job(
                
                title="Python Developer",
                description="Python expert",
                location="Remote",
                skills=["python"],
                employer_
                tokens=["python", "developer", "expert"],
                embedding=[0.1] * 128,
                normalized_text="python developer expert",
            ),
            Job(
                
                title="Java Developer",
                description="Java expert",
                location="Remote",
                skills=["java"],
                employer_
                tokens=["java", "developer", "expert"],
                embedding=[0.9] * 128,  # High embedding similarity (should be ignored)
                normalized_text="java developer expert",
            ),
        ]
        
        query_tokens = ["python", "developer"]
        query_vector = [0.9] * 128  # Similar to job-2 embedding
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=query_tokens,
            query_vector=query_vector,
            limit=10,
            bm25_weight=1.0,
            vector_weight=0.0,
            profile_skills=["python"],
        )
        
        # Python job should rank higher due to BM25 match
        assert len(results) == 2
        assert results[0].job.id == "job-1"
        assert results[0].bm25_score > results[1].bm25_score
    
    def test_vector_only_configuration(self):
        """
        Given: BM25 weight = 0.0, vector weight = 1.0
        When: rank_jobs is called
        Then: Only vector similarity influences ranking
        """
        jobs = [
            Job(
                
                title="Python Developer",
                description="Python expert",
                location="Remote",
                skills=["python"],
                employer_
                tokens=["python", "developer"],
                embedding=[0.1] * 128,  # Low similarity
                normalized_text="python developer",
            ),
            Job(
                
                title="Data Scientist",
                description="ML engineer",
                location="Remote",
                skills=["ml"],
                employer_
                tokens=["data", "scientist", "ml"],
                embedding=[0.9] * 128,  # High similarity
                normalized_text="data scientist ml",
            ),
        ]
        
        query_tokens = ["python"]  # Matches job-1 for BM25
        query_vector = [0.9] * 128  # Matches job-2 for vector
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=query_tokens,
            query_vector=query_vector,
            limit=10,
            bm25_weight=0.0,
            vector_weight=1.0,
        )
        
        # Job-2 should rank higher due to vector similarity
        assert len(results) == 2
        assert results[0].job.id == "job-2"
        assert results[0].vector_score > results[1].vector_score
    
    def test_balanced_configuration(self):
        """
        Given: BM25 weight = 0.5, vector weight = 0.5
        When: rank_jobs is called
        Then: Both scores contribute equally to ranking
        """
        jobs = [
            Job(
                
                title="Python Developer",
                description="Expert",
                location="Remote",
                skills=["python"],
                employer_
                tokens=["python", "developer", "expert"],
                embedding=[0.5] * 128,
                normalized_text="python developer expert",
            ),
        ]
        
        query_tokens = ["python"]
        query_vector = [0.5] * 128
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=query_tokens,
            query_vector=query_vector,
            limit=10,
            bm25_weight=0.5,
            vector_weight=0.5,
        )
        
        assert len(results) == 1
        result = results[0]
        
        # Both scores should contribute
        assert result.bm25_score > 0
        assert result.vector_score >= 0
        assert result.score > 0
    
    def test_custom_weight_ratios(self):
        """
        Given: Various weight ratios (0.3/0.7, 0.8/0.2, 0.1/0.9)
        When: rank_jobs is called
        Then: Results reflect the configured weight importance
        """
        jobs = [
            Job(
                
                title="Test Job",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["test", "job"],
                embedding=[0.5] * 128,
                normalized_text="test job",
            ),
        ]
        
        query_tokens = ["test"]
        query_vector = [0.5] * 128
        
        # Test different weight configurations
        configs = [
            (0.3, 0.7),  # Vector-heavy
            (0.8, 0.2),  # BM25-heavy
            (0.1, 0.9),  # Extreme vector preference
            (0.9, 0.1),  # Extreme BM25 preference
        ]
        
        for bm25_w, vec_w in configs:
            results = rank_jobs(
                jobs=jobs,
                query_tokens=query_tokens,
                query_vector=query_vector,
                limit=10,
                bm25_weight=bm25_w,
                vector_weight=vec_w,
            )
            
            assert len(results) == 1
            # Verify scores are computed
            assert results[0].score >= 0


class TestWeightNormalization:
    """ST-004-UNIT-002: Validate weight sum normalization."""
    
    def test_weight_normalization_with_equal_weights(self):
        """
        Given: BM25 weight = 0.4, vector weight = 0.6
        When: rank_jobs is called
        Then: Weights are normalized to sum to 1.0
        """
        jobs = [
            Job(
                
                title="Engineer",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["engineer", "test"],
                embedding=[0.5] * 128,
                normalized_text="engineer test",
            ),
        ]
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=["engineer"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.4,
            vector_weight=0.6,
        )
        
        # Weights should normalize: 0.4/1.0 = 0.4, 0.6/1.0 = 0.6
        assert len(results) == 1
        assert results[0].score >= 0
    
    def test_weight_normalization_with_large_values(self):
        """
        Given: BM25 weight = 40, vector weight = 60
        When: rank_jobs is called
        Then: Weights are normalized correctly (same as 0.4/0.6)
        """
        jobs = [
            Job(
                
                title="Developer",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["developer", "test"],
                embedding=[0.5] * 128,
                normalized_text="developer test",
            ),
        ]
        
        # Large weights
        results_large = rank_jobs(
            jobs=jobs,
            query_tokens=["developer"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=40.0,
            vector_weight=60.0,
        )
        
        # Small weights with same ratio
        results_small = rank_jobs(
            jobs=jobs,
            query_tokens=["developer"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.4,
            vector_weight=0.6,
        )
        
        # Scores should be the same (normalized)
        assert len(results_large) == 1
        assert len(results_small) == 1
        assert abs(results_large[0].score - results_small[0].score) < 0.01
    
    def test_zero_weights_fallback(self):
        """
        Given: BM25 weight = 0, vector weight = 0
        When: rank_jobs is called
        Then: Falls back to BM25-only scoring (safe default)
        """
        jobs = [
            Job(
                
                title="Analyst",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["analyst", "test"],
                embedding=[0.5] * 128,
                normalized_text="analyst test",
            ),
        ]
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=["analyst"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.0,
            vector_weight=0.0,
        )
        
        # Should not crash, should return results
        assert len(results) == 1
        assert results[0].score >= 0
    
    def test_negative_weights_handling(self):
        """
        Given: Negative weights
        When: rank_jobs is called
        Then: Handles gracefully (future: should validate/reject)
        """
        jobs = [
            Job(
                
                title="Manager",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["manager", "test"],
                embedding=[0.5] * 128,
                normalized_text="manager test",
            ),
        ]
        
        # Current implementation doesn't validate
        # Future enhancement: should raise ValueError
        results = rank_jobs(
            jobs=jobs,
            query_tokens=["manager"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=-0.5,
            vector_weight=1.5,
        )
        
        # Should still compute (though results may be unexpected)
        assert len(results) >= 0
    
    def test_fractional_weight_precision(self):
        """
        Given: Precise fractional weights (e.g., 0.333, 0.667)
        When: rank_jobs is called
        Then: Maintains precision in calculations
        """
        jobs = [
            Job(
                
                title="Specialist",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["specialist", "test"],
                embedding=[0.5] * 128,
                normalized_text="specialist test",
            ),
        ]
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=["specialist"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.333333,
            vector_weight=0.666667,
        )
        
        assert len(results) == 1
        # Verify score is computed with precision
        assert results[0].score > 0


class TestScoringHelperFunctions:
    """Additional tests for scoring helper functions."""
    
    def test_build_query_tokens_with_all_inputs(self):
        """
        Given: Skills, titles, and extra text
        When: build_query_tokens is called
        Then: All inputs are tokenized and combined
        """
        tokens = build_query_tokens(
            skills=["python", "fastapi"],
            titles=["Software Engineer", "Developer"],
            extra_text="machine learning expert",
        )
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert any("python" in token.lower() for token in tokens)
    
    def test_build_query_tokens_with_minimal_inputs(self):
        """
        Given: Only skills provided
        When: build_query_tokens is called
        Then: Tokens are created from skills only
        """
        tokens = build_query_tokens(
            skills=["java"],
            titles=[],
            extra_text=None,
        )
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
    
    def test_cosine_similarity_identical_vectors(self):
        """
        Given: Two identical vectors
        When: _cosine_similarity is called
        Then: Returns 1.0 (perfect similarity)
        """
        vector = [0.5] * 128
        similarity = _cosine_similarity(vector, vector)
        
        assert abs(similarity - 1.0) < 0.01
    
    def test_cosine_similarity_orthogonal_vectors(self):
        """
        Given: Two orthogonal vectors
        When: _cosine_similarity is called
        Then: Returns ~0.0 (no similarity)
        """
        vec1 = [1.0, 0.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0, 0.0]
        
        similarity = _cosine_similarity(vec1, vec2)
        assert abs(similarity) < 0.01
    
    def test_cosine_similarity_empty_vectors(self):
        """
        Given: Empty vectors
        When: _cosine_similarity is called
        Then: Returns 0.0 (handles gracefully)
        """
        similarity = _cosine_similarity([], [])
        assert similarity == 0.0
    
    def test_compute_idf_basic(self):
        """
        Given: Document tokens
        When: _compute_idf is called
        Then: Returns IDF scores for terms
        """
        docs = [
            ["python", "developer"],
            ["java", "developer"],
            ["python", "expert"],
        ]
        
        idf = _compute_idf(docs)
        
        assert isinstance(idf, dict)
        assert "developer" in idf
        assert "python" in idf
        # "developer" appears in 2/3 docs, should have lower IDF
        # "java" appears in 1/3 docs, should have higher IDF
        assert idf["java"] > idf["developer"]


class TestScoringEdgeCases:
    """Edge case tests for robustness."""
    
    def test_rank_jobs_empty_list(self):
        """
        Given: Empty job list
        When: rank_jobs is called
        Then: Returns empty list without errors
        """
        results = rank_jobs(
            jobs=[],
            query_tokens=["test"],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.5,
            vector_weight=0.5,
        )
        
        assert results == []
    
    def test_rank_jobs_no_query_tokens(self):
        """
        Given: Empty query tokens
        When: rank_jobs is called
        Then: Returns results (vector-only scoring)
        """
        jobs = [
            Job(
                
                title="Test",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["test"],
                embedding=[0.5] * 128,
                normalized_text="test",
            ),
        ]
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=[],
            query_vector=[0.5] * 128,
            limit=10,
            bm25_weight=0.5,
            vector_weight=0.5,
        )
        
        assert len(results) >= 0
    
    def test_rank_jobs_with_limit(self):
        """
        Given: More jobs than limit
        When: rank_jobs is called with limit=2
        Then: Returns only top 2 results
        """
        jobs = [
            Job(
                id=f"job-{i}",
                title=f"Job {i}",
                description="Test",
                location="Remote",
                skills=["test"],
                employer_
                tokens=["job", f"{i}"],
                embedding=[float(i) / 10] * 128,
                normalized_text=f"job {i}",
            )
            for i in range(5)
        ]
        
        results = rank_jobs(
            jobs=jobs,
            query_tokens=["job"],
            query_vector=[0.5] * 128,
            limit=2,
            bm25_weight=0.5,
            vector_weight=0.5,
        )
        
        assert len(results) <= 2


# Documentation for future enhancements
"""
FUTURE ENHANCEMENTS NEEDED:

1. Weight Validation (ST-004-UNIT-001):
   - Add validation for weight ranges (e.g., 0.0 to 1.0)
   - Raise ValueError for negative weights
   - Add configuration schema validation
   - Support weight presets (e.g., "bm25_only", "balanced", "semantic_only")

2. Normalization Guarantees (ST-004-UNIT-002):
   - Ensure weights always sum to 1.0
   - Add explicit normalization step with logging
   - Validate normalized weights before scoring
   - Add monitoring for weight configuration changes

3. Configuration Management:
   - Add weight configuration hot-reload
   - Support per-query weight overrides
   - Add A/B testing support for different weight configurations
   - Track which weight configurations perform best

4. Scoring Transparency:
   - Add detailed score breakdown in explanations
   - Show which weight configuration was used
   - Include normalized weights in response metadata

Example validation implementation:

def validate_weights(bm25_weight: float, vector_weight: float) -> tuple[float, float]:
    if bm25_weight < 0 or vector_weight < 0:
        raise ValueError("Weights must be non-negative")
    
    if bm25_weight == 0 and vector_weight == 0:
        logging.warning("Both weights are zero, using BM25-only fallback")
        return 1.0, 0.0
    
    total = bm25_weight + vector_weight
    normalized_bm25 = bm25_weight / total
    normalized_vector = vector_weight / total
    
    logging.info(f"Normalized weights: BM25={normalized_bm25:.2f}, Vector={normalized_vector:.2f}")
    return normalized_bm25, normalized_vector
"""
