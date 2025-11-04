## Problem Solving Session: Low Relevance in Early Recommendations

**Date:** 2025-11-04
**Problem Solver:** Team 4
**Problem Category:** Recommendations / Relevance / Engagement

---

## 🎯 PROBLEM DEFINITION

### Initial Problem Statement

Early AI job recommendations feel off-target, leading to low CTR and weak engagement from seekers.

### Refined Problem Statement

The baseline recommendation pipeline produces insufficiently relevant suggestions for new users (cold start) due to limited structured signals and inconsistent skill/taxonomy normalization, resulting in reduced click-through and apply starts.

### Problem Context

Two-sided Job Portal MVP (Next.js + FastAPI + MongoDB + ChromaDB). Resume upload extracts skills; recommendations combine keyword search and embeddings. Users expect transparent, actionable “Why this job?” explanations.

### Success Criteria

- +20–30% CTR on recommended jobs within 2 weeks of deployment
- +15% apply-start rate from recommendations
- >70% perceived relevance in user feedback prompts

---

## 🔍 DIAGNOSIS AND ROOT CAUSE ANALYSIS

### Problem Boundaries (Is/Is Not)

- IS: New users with little interaction history; sparse/unclean resumes; noisy job postings.
- IS NOT: Logged-in power users with rich histories; ATS import at this stage.
- OCCURS: On first session and first 3 recommendation refreshes.
- DOESN’T OCCUR: After users curate skills/preferences and provide feedback.

### Root Cause Analysis

- Symptoms: Irrelevant titles; seniority mismatch; missing core skills; generic listings.
- Causes: Weak normalization (titles/skills); cold start; limited features for ranking; noisy text.
- Root Causes: Lack of robust ontology; insufficient hybrid scoring; no learn-to-rank; minimal feedback loop utilization.

### Contributing Factors

- Resume parsing errors; employer postings lacking structure; synonyms/aliases (JS vs. JavaScript).

### System Dynamics

- Positive loop: Better matches → more clicks/applies → better feedback → improved model.
- Negative loop: Poor matches → low engagement → scarce signals → stagnant quality.

---

## 📊 ANALYSIS

### Force Field Analysis

**Driving Forces (Supporting Solution):**
Clear user intent via resume; embeddings for semantic similarity; strong appetite for explainability.

**Restraining Forces (Blocking Solution):**
Data sparsity; ontology gaps; cold start; potential bias; compute limits.

### Constraint Identification

Privacy and fairness requirements; limited initial dataset; must remain explainable and fast.

### Key Insights

Hybrid retrieval + normalization + user feedback is the fastest path to reliable relevance.

---

## 💡 SOLUTION GENERATION

### Methods Used

TRIZ principles; Morphological Analysis; Assumption Busting; Reverse Brainstorming.

### Generated Solutions

- Hybrid retriever (BM25 + dense embeddings) with weighted scoring.
- Skill/title normalization (alias table + ontology) at index time.
- Explainability: top contributing skills/terms; confidence score bands.
- Cold-start booster: resume-derived preferences + location + recency.
- Feedback capture: thumbs up/down + “not relevant” reasons → learning signals.

### Creative Alternatives

- Collaborative filtering v0 using co-apply patterns (later phase).
- Reranker with small learn-to-rank model trained on click/apply data.

---

## ⚖️ SOLUTION EVALUATION

### Evaluation Criteria

Effectiveness; explainability; feasibility; latency; privacy/fairness; engineering effort.

### Solution Analysis

- Hybrid retrieval improves recall/precision; explainable with token/skill attributions.
- Ontology raises consistency and reduces mismatch.
- Feedback loop enables continuous improvement with low overhead.

### Recommended Solution

Hybrid recommendations v1: BM25 + dense embeddings + normalization + explainability + feedback signals.

### Rationale

Best balance of impact, speed, and transparency for MVP timelines.

---

## 🚀 IMPLEMENTATION PLAN

### Implementation Approach

Pilot on subset of users; instrument metrics; iterate weekly.

### Action Steps

1. Build normalization tables (skills/titles); index jobs/resumes with normalized fields.
2. Implement BM25 + embeddings scoring with tunable weights.
3. Add explainability payload (top terms/skills contributing to score).
4. Add feedback API and UI; log signals.
5. Ship; review metrics; adjust weights; consider light reranker.

### Timeline and Milestones

2 weeks to v1 pilot; weekly tuning cycles for 3–4 weeks.

### Resource Requirements

Engineer (backend), Engineer (frontend), part-time data engineer; embedding inference budget.

### Responsible Parties

Team 4 (backend, frontend); advisor for metrics/fairness.

---

## 📈 MONITORING AND VALIDATION

### Success Metrics

CTR on recs; apply-start from recs; time-to-first relevant click; satisfaction score.

### Validation Plan

A/B test vs. baseline keyword recommender; qualitative surveys; log-based audits.

### Risk Mitigation

Bias/fairness checks; fallback to keyword-only if embedding service degrades; watchdog on latency.

### Adjustment Triggers

CTR drop >10% week-over-week; latency p95 > 400ms; complaints about relevance/explanations.

---

## 📝 LESSONS LEARNED

### Key Learnings

Normalization and explainability are non-negotiable for trust; feedback loops compound quickly.

### What Worked

Hybrid retrieval; simple, transparent explanation UI; fast iterations.

### What to Avoid

Overfitting to sparse data; shipping a black-box model without guardrails.

---

_Generated using BMAD Creative Intelligence Suite - Problem Solving Workflow_

