# Job Portal Documentation

This directory contains all project documentation organized by category.

## 🆕 Recent Updates (November 2024)

### Service Management Enhancements
- **New unified management script**: `manage.sh` consolidates all service operations
- **Automatic port cleanup**: Restart commands now automatically free up blocked ports
- **Deprecated scripts removed**: `start.sh` and `cleanup-services.sh` no longer needed
- **Documentation organized**: All `.md` files moved to `docs/` for better structure

### Key Improvements
- ✅ Single command to start/stop/restart all services
- ✅ Automatic cleanup of orphaned processes on restart
- ✅ Better error handling and troubleshooting
- ✅ Comprehensive documentation with categorized index

See [SCRIPT-CLEANUP-SUMMARY.md](SCRIPT-CLEANUP-SUMMARY.md) and [CHANGELOG.md](CHANGELOG.md) for complete details.

---

## Quick Links

- [Quick Start Guide](quick-start.md) - Get started with the project
- [Service Management Guide](service-management-guide.md) - Managing services with manage.sh
- [Product Requirements](PRD.md) - Full product requirements document
- [Architecture](architecture.md) - System architecture and design
- [Tech Spec](tech-spec.md) - Technical specifications

## Directory Structure

### Core Documentation
- `PRD.md` - Product Requirements Document
- `architecture.md` - System architecture overview
- `tech-spec.md` - Technical specifications
- `ux-design.md` - User experience design guidelines

### Implementation
- `observability-implementation.md` - Observability and monitoring setup
- `observability-readme.md` - Observability usage guide
- `st-013-015-readme.md` - Story 013-015 implementation guide
- `5-stories-implementation-summary.md` - Summary of first 5 stories
- `ALL-STORIES-COMPLETE.md` - Complete stories documentation
- `ST-013-015-implementation-summary.md` - Stories 13-15 implementation
- `ST-014-implementation-summary.md` - Story 14 implementation

### Epics
- `epics.md` - All epics overview
- `epic-auth.md` - Authentication epic
- `epic-onboarding-profile.md` - Onboarding and profile epic
- `epic-recommendations-v1.md` - Recommendations system epic
- `epic-employer-inbox-scheduling.md` - Employer inbox and scheduling epic
- `epic-notifications.md` - Notifications system epic
- `epic-observability.md` - Observability epic

### Stories
Stories are organized in the `stories/` subdirectory.

### Sprints
Sprint artifacts are organized in the `sprints/` subdirectory:
- `sprints/sprint-1/` - Sprint 1 deliverables, gate checklists, test runbooks

### Design & Planning
- `design-thinking-2025-11-04.md` - Design thinking session
- `brainstorming-session-results-2025-11-04.md` - Brainstorming outputs
- `problem-solution-2025-11-04.md` - Problem-solution fit analysis
- `story-2025-11-04.md` - Story creation session
- `sprint-plan-sprint-1.md` - Sprint 1 planning

### Validation
- `PRD-validation.md` - PRD validation results
- `architecture-validation.md` - Architecture validation
- `bmm-readiness-assessment-2025-11-04.md` - BMM readiness assessment

### Status Tracking
- `sprint-status.yaml` - Current sprint status
- `bmm-workflow-status.yaml` - BMM workflow status

### Recent Additions (November 2024)
- `service-management-guide.md` - Complete service management documentation
- `MANAGE-QUICK-REFERENCE.md` - Quick command reference for manage.sh
- `CHANGELOG.md` - Service management version history
- `TROUBLESHOOTING-404.md` - Troubleshooting port conflicts and 404 errors
- `SOLUTION-PORT-CLEANUP.md` - Port cleanup solution overview
- `RESTART-ENHANCEMENT-SUMMARY.md` - Technical details on restart enhancements
- `SCRIPT-CLEANUP-SUMMARY.md` - Documentation of deprecated script removal
- `FILE-ORGANIZATION-SUMMARY.md` - File reorganization documentation
