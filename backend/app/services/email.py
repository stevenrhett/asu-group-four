from dataclasses import dataclass, field
from typing import List, Optional

from app.core.config import settings


@dataclass
class EmailAttachment:
    filename: str
    content: str  # assume text or base64 string
    mimetype: str = "application/octet-stream"


@dataclass
class EmailMessage:
    to: List[str]
    subject: str
    body: str
    attachments: List[EmailAttachment] = field(default_factory=list)
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)


EMAIL_OUTBOX: List[EmailMessage] = []


def clear_email_outbox():
    EMAIL_OUTBOX.clear()


def send_email(message: EmailMessage) -> None:
    """
    Provider-agnostic email sender.

    For now we record all outgoing messages in EMAIL_OUTBOX so tests can assert
    behaviour. In production, replace this stub with a provider integration
    using settings.email_provider.
    """

    if not message.to:
        # No recipients, skip send
        return

    EMAIL_OUTBOX.append(message)
