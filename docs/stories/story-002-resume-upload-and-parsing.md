# Story: Resume Upload & Parsing

ID: ST-002  
Epic: Onboarding & Profile  
Owner: TBD  
Status: drafted

## Description
Allow seekers to upload a resume (PDF/DOCX) and parse into structured data (skills, titles, years, education).

## Acceptance Criteria
1. Given a PDF/DOCX, when uploaded, then file is stored securely and parsed successfully or a clear error is shown.
2. Given a successful parse, then extracted skills/titles populate the profile draft for user confirmation.
3. Given PII, then it is handled per privacy guidelines; raw file is not exposed publicly.

## Technical Notes
- Backend parsing service; library selection TBD; extract skills with simple rules + fallback
- Store normalized skills for downstream recommendations

## Dependencies
- ST-001 Auth & JWT

## Tasks
- [ ] Upload endpoint and storage
- [ ] Parser integration and mappers
- [ ] Profile draft update
- [ ] Unit/integration tests

## FR Coverage
- FR-002 Resume upload and parsing
