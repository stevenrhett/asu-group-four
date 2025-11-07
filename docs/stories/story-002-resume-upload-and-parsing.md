# Story: Resume Upload & Parsing

ID: ST-002  
Epic: Onboarding & Profile  
Owner: TBD  
Status: in-review

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
- [x] Upload endpoint and storage
- [x] Parser integration and mappers
- [x] Profile draft update
- [x] Unit/integration tests

## FR Coverage
- FR-002 Resume upload and parsing
