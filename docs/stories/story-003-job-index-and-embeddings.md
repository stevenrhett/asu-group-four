# Story: Job Index & Embeddings

ID: ST-003  
Epic: Recommendations v1  
Owner: TBD  
Status: drafted

## Description
Create an index for jobs (and optional seeker profile vectors) with normalized fields and dense embeddings for semantic matching.

## Acceptance Criteria
1. Given job postings, when indexed, then normalized text and embeddings are stored and searchable.
2. Given a seeker profile, when generating recommendations, then the system can query BM25 and embeddings.
3. Given failures, then retries/backoff and logging are in place.

## Technical Notes
- ChromaDB; OpenAI or local embeddings (configurable); text normalization and alias tables

## Dependencies
- ST-002 Resume Parsing (normalized skills)

## Tasks
- [ ] Normalization tables (skills/titles)
- [ ] Indexer job and schema
- [ ] Embedding integration and batching
- [ ] Unit tests and data fixtures

## FR Coverage
- FR-004 Recommendation engine v1 (index foundation)
