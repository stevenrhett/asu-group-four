# Story: Hybrid Scoring & Ranking

ID: ST-004  
Epic: Recommendations v1  
Owner: TBD  
Status: in-review

## Description
Combine BM25 lexical scores with dense embedding similarity using tunable weights; return top-N ranked jobs.

## Acceptance Criteria
1. Given a query/profile, when scoring, then ranked results incorporate both BM25 and embeddings per configured weights.
2. Given missing embeddings or errors, then the system gracefully falls back to BM25.
3. Given experiments, then weights can be tuned without redeploying core services.

## Technical Notes
- Weighted linear combination; feature flags/config

## Dependencies
- ST-003 Job Index & Embeddings

## Tasks
- [x] Score combiner implementation
- [x] Config for weights and fallbacks
- [x] Unit tests

## FR Coverage
- FR-004 Recommendation engine v1 (scoring)
