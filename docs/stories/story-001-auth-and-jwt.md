# Story: Auth & JWT (seekers/employers)

ID: ST-001  
Epic: Authentication & Roles  
Owner: TBD  
Status: drafted

## Description
Implement secure registration/login with JWT, password hashing, and role claim (seeker/employer).

## Acceptance Criteria
1. Given a new user, when registering, then password is hashed (bcrypt) and user receives a JWT on login.
2. Given a JWT, when accessing protected endpoints, then role claim is validated and unauthorized requests are rejected with 401.
3. Given invalid credentials, then login fails with 401 and no token is issued.

## Technical Notes
- FastAPI + python-jose, passlib[bcrypt]
- User model: email, hashed_password, role, created_at
- Token: short-lived access, refresh optional later

## Dependencies
None

## Tasks
- [ ] User model and DB collection (Beanie)
- [ ] Hash/verify helpers
- [ ] Register/Login routes + tests
- [ ] JWT middleware + role check dependency

## FR Coverage
- FR-001 Authentication and Authorization
