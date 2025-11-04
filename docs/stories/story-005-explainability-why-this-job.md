# Story: Explainability - "Why this job?"

ID: ST-005  
Epic: Recommendations v1  
Owner: TBD  
Status: drafted

## Description
Expose top contributing skills/terms and brief rationale for each recommendation to increase trust and clarity.

## Acceptance Criteria
1. Given a recommended job, when displayed, then a visible explanation lists key matching skills/terms.
2. Given a user click on details, then an expanded explanation shows contribution weights or tags.
3. Given no explanation available, then a fallback message appears without breaking layout.

## Technical Notes
- Capture attribution data during scoring; UI component for explanation chips

## Dependencies
- ST-004 Hybrid Scoring & Ranking

## Tasks
- [ ] Attribution payload in scoring response
- [ ] UI component for explanation
- [ ] Tests for presence/absence cases

## FR Coverage
- FR-004 Recommendation engine v1 (explainability)
