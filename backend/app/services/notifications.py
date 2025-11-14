from typing import Tuple

from app.models.application import Application
from app.models.user import User
from app.services.email import EmailMessage, send_email

STATUS_SUBJECTS = {
    "applied": "Application received",
    "viewed": "Your application was viewed",
    "shortlisted": "You're shortlisted!",
    "interview": "Interview invitation",
    "rejected": "Application update",
}

STATUS_BODY_TEMPLATES = {
    "applied": "Hi {seeker_email},\n\nThanks for applying. We'll update you as soon as the employer reviews your application.",
    "viewed": "Hi {seeker_email},\n\nGood news! {employer_email} viewed your application for {job_title}.",
    "shortlisted": "Hi {seeker_email},\n\nYou're shortlisted for {job_title}. Expect next steps soon.",
    "interview": "Hi {seeker_email},\n\nYou're invited to an interview for {job_title}. Check your inbox for scheduling details.",
    "rejected": "Hi {seeker_email},\n\nThanks for your interest in {job_title}. The team has decided to move forward with other candidates.",
}

EMPLOYER_CONFIRM_SUBJECTS = {
    "shortlisted": "Candidate shortlisted confirmation",
    "interview": "Interview invitation sent",
}

EMPLOYER_CONFIRM_BODIES = {
    "shortlisted": "You shortlisted {seeker_email} for {job_title}. We've notified the candidate.",
    "interview": "You invited {seeker_email} to interview for {job_title}. We've sent the candidate the details.",
}


def build_status_email(
    application: Application,
    seeker: User,
    employer_email: str,
    job_title: str,
) -> Tuple[str, str]:
    template = STATUS_BODY_TEMPLATES.get(application.status, "Status update for {job_title}.")
    subject = STATUS_SUBJECTS.get(application.status, f"Application status: {application.status}")
    body = template.format(
        seeker_email=seeker.email,
        employer_email=employer_email,
        job_title=job_title,
    )
    return subject, body


def build_employer_confirmation(application: Application, seeker: User, job_title: str) -> Tuple[str, str]:
    subject = EMPLOYER_CONFIRM_SUBJECTS.get(application.status, "")
    body_template = EMPLOYER_CONFIRM_BODIES.get(application.status, "")
    if not subject or not body_template:
        return "", ""
    body = body_template.format(seeker_email=seeker.email, job_title=job_title)
    return subject, body


def dispatch_status_notifications(
    application: Application,
    seeker: User,
    employer: User,
    job_title: str,
) -> None:
    subject, body = build_status_email(application, seeker, employer.email, job_title)
    send_email(EmailMessage(to=[seeker.email], subject=subject, body=body))

    confirm_subject, confirm_body = build_employer_confirmation(application, seeker, job_title)
    if confirm_subject and confirm_body:
        send_email(EmailMessage(to=[employer.email], subject=confirm_subject, body=confirm_body))
