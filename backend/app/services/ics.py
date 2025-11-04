from datetime import datetime
from typing import Optional
from uuid import uuid4


def _format_datetime(dt_iso: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_iso.replace("Z", "+00:00"))
    except ValueError:
        # fallback: return original string
        return dt_iso
    return dt.strftime("%Y%m%dT%H%M%SZ")


def generate_ics(
    title: str,
    start_iso: str,
    end_iso: str,
    location: Optional[str],
    description: Optional[str] = None,
    uid: Optional[str] = None,
) -> str:
    uid_value = uid or f"{uuid4()}@asu-group-four.job-portal"
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dtstart = _format_datetime(start_iso)
    dtend = _format_datetime(end_iso)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ASU Group Four//Job Portal//EN",
        "BEGIN:VEVENT",
        f"UID:{uid_value}",
        f"DTSTAMP:{dtstamp}",
        f"SUMMARY:{title}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"LOCATION:{location or ''}",
    ]
    if description:
        lines.append(f"DESCRIPTION:{description}")

    lines.extend(["END:VEVENT", "END:VCALENDAR"])
    return "\n".join(lines)
