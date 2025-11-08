# Story: Notification Preferences

ID: ST-018  
Epic: Notifications  
Owner: TBD  
Status: draft  
Sprint: Sprint 2

## Description
Allow both job seekers and employers to configure their notification preferences across different channels (email, in-app) and categories (applications, status changes, system alerts). Provides granular control over notification frequency and types.

## User Stories

### As a Job Seeker:
- I want to control when I receive job recommendation emails
- I want to toggle notifications for application status changes
- I want to set digest frequency (real-time, daily, weekly)

### As an Employer:
- I want to control notifications for new applications
- I want to configure alerts for candidate messages
- I want to set quiet hours so I don't get notifications outside work hours
- I want to choose between email and in-app notifications per category

## Acceptance Criteria

1. **Given** a logged-in user, **when** they navigate to /settings/notifications, **then** they see all available notification categories with toggles for email and in-app channels

2. **Given** a job seeker, **when** they view notification preferences, **then** they see categories for:
   - Job recommendations
   - Application status updates
   - System announcements
   - With options: Email (on/off), In-app (on/off), Frequency (real-time/daily/weekly)

3. **Given** an employer, **when** they view notification preferences, **then** they see categories for:
   - New applications received
   - Candidate messages
   - Application status changes (their own updates)
   - Job posting expirations/warnings
   - Interview reminders
   - System announcements
   - With options: Email (on/off), In-app (on/off), Digest frequency

4. **Given** an employer sets quiet hours (e.g., 6 PM - 8 AM), **when** a notification event occurs during quiet hours, **then** notifications are queued and sent at the next available time (8 AM) or in next digest

5. **Given** a user updates their preferences, **when** they click Save, **then** changes are persisted and they receive a confirmation message

6. **Given** notification preferences are disabled for a category, **when** an event in that category occurs, **then** no notification is sent via the disabled channel(s)

## Technical Notes

**Frontend (Next.js):**
- New route: `/app/settings/notifications/page.tsx`
- Can be a tab within main Settings page or standalone
- Components:
  - `NotificationCategoryCard` - Displays category with channel toggles
  - `QuietHoursSelector` - Time range picker (employer only)
  - `DigestFrequencySelector` - Dropdown (real-time, daily digest, weekly digest)

**Backend (FastAPI):**
- New routes in `/api/v1/routes/users.py`:
  - `GET /api/users/me/notifications/preferences` - Get current preferences
  - `PUT /api/users/me/notifications/preferences` - Update preferences
  
**Data Model:**
- Add to User model or create separate `NotificationPreferences` model:
  ```python
  class NotificationPreferences(BaseModel):
      user_id: str
      email_enabled: bool = True
      in_app_enabled: bool = True
      
      # Category preferences (dict with category: {email: bool, in_app: bool, frequency: str})
      preferences: Dict[str, Dict[str, Any]] = {}
      
      # Employer-specific
      quiet_hours_start: Optional[str] = None  # "18:00"
      quiet_hours_end: Optional[str] = None    # "08:00"
      timezone: str = "UTC"
  ```

**Default Preferences:**
- All notifications ON by default
- Frequency: real-time for important events, daily digest for recommendations
- No quiet hours by default

**Integration Points:**
- Ties into ST-008 (Status Change Emails) - check preferences before sending
- Email service needs to respect these settings
- Future in-app notification system will use these preferences

## Dependencies
- ST-001: Auth & JWT (user identity)
- ST-008: Status Change Emails (integration point)
- ST-016: Account Settings (shares settings page structure)

## Tasks
- [ ] Design notification preferences UI (mobile responsive)
- [ ] Backend: Create NotificationPreferences model
- [ ] Backend: Implement GET/PUT preferences endpoints
- [ ] Backend: Add preference checking logic to email service
- [ ] Backend: Implement quiet hours logic
- [ ] Frontend: Build notification preferences page/tab
- [ ] Frontend: Implement category toggle switches
- [ ] Frontend: Implement quiet hours time picker (employer)
- [ ] Frontend: Implement digest frequency selector
- [ ] Update email service to check preferences before sending
- [ ] Unit tests for preferences endpoints
- [ ] Unit tests for quiet hours logic
- [ ] Integration test with ST-008 email sending
- [ ] E2E test for preference updates
- [ ] Documentation for notification categories

## Out of Scope (Future Enhancements)
- SMS/text notifications
- Push notifications (mobile app)
- Notification templates customization
- Team-level notification routing (advanced employer feature)
- Notification history/log viewer

## FR Coverage
- New Feature: Notification Management & Preferences
- Enhances: FR-008 (Status Change Notifications)

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Code reviewed and merged
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration with ST-008 verified
- [ ] E2E test for both seeker and employer flows
- [ ] Works across different timezones (quiet hours)
- Mobile responsive UI
- [ ] Documentation updated

## Estimates
**Complexity:** Medium  
**Story Points:** 5  
**Sprint:** Sprint 2

