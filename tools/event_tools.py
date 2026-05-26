from datetime import datetime
from pathlib import Path

from tools.email_tools import send_system_email


ADMIN_EMAIL = "lkprofessionals234@gmail.com"
EVENT_LOG = Path("storage/events/events.log")


def emit_event(event_type: str, title: str, details: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)

    with open(EVENT_LOG, "a") as f:
        f.write(f"[{timestamp}] {event_type} | {title} | {details}\n")

    subject = f"[JARVIS] {event_type} - {title}"

    body = f"""
JARVIS EVENT NOTIFICATION

Timestamp:
{timestamp}

Event Type:
{event_type}

Title:
{title}

Details:
{details}
"""

    return send_system_email(
        to_email=ADMIN_EMAIL,
        subject=subject,
        body=body,
    )