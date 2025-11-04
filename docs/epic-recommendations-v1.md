# Epic: Recommendations v1 (Hybrid + Explainability + Feedback)

## Goal
Serve relevant, explainable job recommendations quickly for new and returning users.

## Outcome Metrics
- +20–30% CTR on recommended jobs within 2 weeks
- >70% perceived relevance from in-product prompts

## Scope
- Index jobs and resumes with normalized skills/titles
- Hybrid retrieval (BM25 + embeddings) with tunable weights
- Explainability payload (top contributing skills/terms)
- Feedback capture (thumbs up/down, reason codes)

## Out of Scope
- Learn-to-rank reranker; collaborative filtering (post-MVP)

## Stories
- [ ] ST-003 Job Index & Embeddings
- [ ] ST-004 Hybrid Scoring & Ranking
- [ ] ST-005 Explainability: "Why this job?"
- [ ] ST-006 Feedback Capture & Logging

---

### Dependencies
- ST-002 Resume Parsing (skills extraction)

