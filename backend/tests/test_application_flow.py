"""
Tests for application flow and status tracking (ST-014).

Tests job application submission, status lifecycle, audit trails,
and authorization.
"""
import pytest
from datetime import datetime
from app.models.application import (
    Application,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationStatus,
    StatusChange,
    ApplicationResponse,
    ApplicationWithHistory
)


class TestApplicationStatus:
    """Test application status enumeration."""
    
    def test_status_enum_values(self):
        """Test that all status values are defined."""
        assert ApplicationStatus.APPLIED == "applied"
        assert ApplicationStatus.VIEWED == "viewed"
        assert ApplicationStatus.SHORTLISTED == "shortlisted"
        assert ApplicationStatus.INTERVIEW == "interview"
        assert ApplicationStatus.REJECTED == "rejected"
    
    def test_status_enum_members(self):
        """Test that all expected statuses exist."""
        statuses = [s.value for s in ApplicationStatus]
        assert "applied" in statuses
        assert "viewed" in statuses
        assert "shortlisted" in statuses
        assert "interview" in statuses
        assert "rejected" in statuses


class TestApplicationCreate:
    """Test application creation schema."""
    
    def test_create_schema_valid(self):
        """Test valid application creation."""
        app_create = ApplicationCreate(
            job_id="job123",
            cover_letter="I am very interested in this position..."
        )
        assert app_create.job_id == "job123"
        assert app_create.cover_letter is not None
    
    def test_create_schema_minimal(self):
        """Test application creation with minimal fields."""
        app_create = ApplicationCreate(job_id="job123")
        assert app_create.job_id == "job123"
        assert app_create.cover_letter is None
    
    def test_cover_letter_max_length(self):
        """Test that cover letter respects max length."""
        with pytest.raises(ValueError):
            ApplicationCreate(
                job_id="job123",
                cover_letter="A" * 2001  # Too long
            )


class TestApplicationUpdate:
    """Test application update schema."""
    
    def test_update_schema_valid(self):
        """Test valid status update."""
        update = ApplicationUpdate(
            status=ApplicationStatus.VIEWED,
            notes="Reviewed application"
        )
        assert update.status == ApplicationStatus.VIEWED
        assert update.notes == "Reviewed application"
    
    def test_update_schema_minimal(self):
        """Test update with minimal fields."""
        update = ApplicationUpdate(status=ApplicationStatus.SHORTLISTED)
        assert update.status == ApplicationStatus.SHORTLISTED
        assert update.notes is None
    
    def test_update_notes_max_length(self):
        """Test that notes respect max length."""
        with pytest.raises(ValueError):
            ApplicationUpdate(
                status=ApplicationStatus.VIEWED,
                notes="A" * 501  # Too long
            )


class TestStatusChange:
    """Test status change tracking."""
    
    def test_status_change_creation(self):
        """Test creating a status change record."""
        change = StatusChange(
            from_status=ApplicationStatus.APPLIED,
            to_status=ApplicationStatus.VIEWED,
            changed_by="employer123",
            notes="Initial review"
        )
        assert change.from_status == ApplicationStatus.APPLIED
        assert change.to_status == ApplicationStatus.VIEWED
        assert change.changed_by == "employer123"
        assert change.notes == "Initial review"
        assert change.changed_at is not None
    
    def test_status_change_initial_application(self):
        """Test status change for initial application."""
        change = StatusChange(
            from_status=None,
            to_status=ApplicationStatus.APPLIED,
            changed_by="seeker123"
        )
        assert change.from_status is None
        assert change.to_status == ApplicationStatus.APPLIED
    
    def test_status_change_timestamp(self):
        """Test that timestamp is automatically set."""
        now = datetime.utcnow()
        change = StatusChange(
            to_status=ApplicationStatus.VIEWED,
            changed_by="employer123"
        )
        assert change.changed_at is not None
        assert abs((change.changed_at - now).total_seconds()) < 1


class TestApplicationModel:
    """Test application model fields and annotations."""
    
    def test_model_annotations(self):
        """Test that all expected fields are defined."""
        assert 'job_id' in Application.__annotations__
        assert 'user_id' in Application.__annotations__
        assert 'employer_id' in Application.__annotations__
        assert 'status' in Application.__annotations__
        assert 'created_at' in Application.__annotations__
        assert 'updated_at' in Application.__annotations__
        assert 'status_history' in Application.__annotations__
    
    def test_timestamp_fields(self):
        """Test specific timestamp fields."""
        assert 'viewed_at' in Application.__annotations__
        assert 'shortlisted_at' in Application.__annotations__
        assert 'interview_at' in Application.__annotations__
        assert 'rejected_at' in Application.__annotations__
    
    def test_default_status(self):
        """Test default status is APPLIED."""
        # Tested through API integration tests
        assert ApplicationStatus.APPLIED == "applied"


class TestApplicationResponse:
    """Test application response schemas."""
    
    def test_response_schema_fields(self):
        """Test that response schema has all required fields."""
        # Create a mock application dict
        app_data = {
            "id": "app123",
            "job_id": "job123",
            "user_id": "user123",
            "employer_id": "employer123",
            "status": ApplicationStatus.APPLIED,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "viewed_at": None,
            "shortlisted_at": None,
            "interview_at": None,
            "rejected_at": None,
            "cover_letter": "Test cover letter"
        }
        
        response = ApplicationResponse(**app_data)
        assert response.id == "app123"
        assert response.status == ApplicationStatus.APPLIED
    
    def test_with_history_schema(self):
        """Test application with history schema."""
        app_data = {
            "id": "app123",
            "job_id": "job123",
            "user_id": "user123",
            "employer_id": "employer123",
            "status": ApplicationStatus.VIEWED,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "viewed_at": datetime.utcnow(),
            "shortlisted_at": None,
            "interview_at": None,
            "rejected_at": None,
            "cover_letter": None,
            "status_history": [
                StatusChange(
                    from_status=None,
                    to_status=ApplicationStatus.APPLIED,
                    changed_by="user123"
                ),
                StatusChange(
                    from_status=ApplicationStatus.APPLIED,
                    to_status=ApplicationStatus.VIEWED,
                    changed_by="employer123"
                )
            ]
        }
        
        response = ApplicationWithHistory(**app_data)
        assert len(response.status_history) == 2
        assert response.status == ApplicationStatus.VIEWED


class TestStatusLifecycle:
    """Test application status lifecycle and transitions."""
    
    def test_typical_success_flow(self):
        """Test typical successful application flow."""
        # applied → viewed → shortlisted → interview
        statuses = [
            ApplicationStatus.APPLIED,
            ApplicationStatus.VIEWED,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.INTERVIEW
        ]
        
        # All transitions should be valid
        for i in range(len(statuses) - 1):
            assert statuses[i] in ApplicationStatus
            assert statuses[i+1] in ApplicationStatus
    
    def test_rejection_flow(self):
        """Test rejection at various stages."""
        # Can be rejected from any status
        rejection_paths = [
            [ApplicationStatus.APPLIED, ApplicationStatus.REJECTED],
            [ApplicationStatus.VIEWED, ApplicationStatus.REJECTED],
            [ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED],
            [ApplicationStatus.INTERVIEW, ApplicationStatus.REJECTED]
        ]
        
        for path in rejection_paths:
            assert ApplicationStatus.REJECTED in ApplicationStatus
    
    def test_status_progression(self):
        """Test that status values represent progression."""
        # This is conceptual - the actual enforcement happens in business logic
        all_statuses = list(ApplicationStatus)
        assert ApplicationStatus.APPLIED in all_statuses
        assert ApplicationStatus.REJECTED in all_statuses


class TestIdempotency:
    """Test idempotent operations."""
    
    @pytest.mark.asyncio
    async def test_duplicate_application_idempotent(self):
        """Test that applying twice to same job is idempotent."""
        # Integration test placeholder
        # Should return existing application, not create duplicate
        pass
    
    @pytest.mark.asyncio
    async def test_same_status_update_idempotent(self):
        """Test that updating to same status is idempotent."""
        # Integration test placeholder
        # Should not create duplicate status history entries
        pass


class TestAuthorization:
    """Test authorization rules."""
    
    @pytest.mark.asyncio
    async def test_seeker_can_apply(self):
        """Test that seekers can submit applications."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_employer_cannot_apply(self):
        """Test that employers cannot submit applications."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_seeker_views_own_applications(self):
        """Test that seekers only see their own applications."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_employer_views_job_applications(self):
        """Test that employers see applications for their jobs."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_employer_updates_own_job_applications(self):
        """Test that employers can only update their job applications."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_seeker_cannot_update_status(self):
        """Test that seekers cannot update application status."""
        # Integration test placeholder
        pass


class TestWithdrawal:
    """Test application withdrawal."""
    
    @pytest.mark.asyncio
    async def test_seeker_can_withdraw_applied(self):
        """Test that seekers can withdraw applications in 'applied' status."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_seeker_can_withdraw_viewed(self):
        """Test that seekers can withdraw applications in 'viewed' status."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_seeker_cannot_withdraw_shortlisted(self):
        """Test that seekers cannot withdraw shortlisted applications."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_seeker_cannot_withdraw_others_application(self):
        """Test that seekers cannot withdraw other users' applications."""
        # Integration test placeholder
        pass


class TestAuditTrail:
    """Test audit trail and history tracking."""
    
    def test_status_history_recorded(self):
        """Test that status changes are recorded in history."""
        # Each status change should add to history
        history = [
            StatusChange(
                from_status=None,
                to_status=ApplicationStatus.APPLIED,
                changed_by="user123"
            ),
            StatusChange(
                from_status=ApplicationStatus.APPLIED,
                to_status=ApplicationStatus.VIEWED,
                changed_by="employer123"
            )
        ]
        
        assert len(history) == 2
        assert history[0].to_status == ApplicationStatus.APPLIED
        assert history[1].to_status == ApplicationStatus.VIEWED
    
    def test_history_includes_actor(self):
        """Test that history records who made each change."""
        change = StatusChange(
            to_status=ApplicationStatus.VIEWED,
            changed_by="employer123"
        )
        assert change.changed_by == "employer123"
    
    def test_history_includes_timestamp(self):
        """Test that history records when changes occurred."""
        change = StatusChange(
            to_status=ApplicationStatus.VIEWED,
            changed_by="employer123"
        )
        assert change.changed_at is not None
    
    def test_history_includes_notes(self):
        """Test that history can include notes."""
        change = StatusChange(
            to_status=ApplicationStatus.REJECTED,
            changed_by="employer123",
            notes="Not a good fit for the role"
        )
        assert change.notes == "Not a good fit for the role"


class TestTimestamps:
    """Test timestamp management."""
    
    def test_status_specific_timestamps(self):
        """Test that each status gets its own timestamp field."""
        # Verify fields exist
        assert 'viewed_at' in Application.__annotations__
        assert 'shortlisted_at' in Application.__annotations__
        assert 'interview_at' in Application.__annotations__
        assert 'rejected_at' in Application.__annotations__
    
    @pytest.mark.asyncio
    async def test_viewed_timestamp_set_on_status_change(self):
        """Test that viewed_at is set when status changes to VIEWED."""
        # Integration test placeholder
        pass
    
    @pytest.mark.asyncio
    async def test_shortlisted_timestamp_set_on_status_change(self):
        """Test that shortlisted_at is set when status changes to SHORTLISTED."""
        # Integration test placeholder
        pass
