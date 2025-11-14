# Story: Metrics Dashboard (MVP)

ID: ST-012  
Epic: Observability & Metrics  
Owner: TBD  
Status: drafted

## Description
Create a simple dashboard to visualize core KPIs: CTR on recommendations, apply conversion, time-to-shortlist.

## Acceptance Criteria
1. Given logged events, then dashboard shows CTR (views vs clicks) over time.
2. Given apply events, then dashboard shows conversion rate and trend.
3. Given shortlist events, then dashboard shows median time-to-shortlist.

## Technical Notes
- Start with simple export or in-app page; refine later

## Dependencies
- ST-011 Event Schema & Logging

## Tasks
- [ ] Data aggregation for KPIs
- [ ] Minimal dashboard UI or report
- [ ] Tests

## FR Coverage
- FR-009 Metrics and logging

