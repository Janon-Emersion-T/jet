from datetime import datetime
from pathlib import Path

from tools.email_tools import send_system_email
from tools.notification_config import load_notification_settings


EVENT_LOG = Path("storage/events/events.log")


def _needs_attention(event_type: str, requires_attention: bool | None) -> bool:
    if requires_attention is not None:
        return requires_attention
    settings = load_notification_settings()
    event = event_type.upper()
    return any(marker in event for marker in settings["attention_event_types"])


def emit_event(event_type: str, title: str, details: str, requires_attention: bool | None = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    settings = load_notification_settings()
    attention = _needs_attention(event_type, requires_attention)

    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)

    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {event_type} | attention={attention} | {title} | {details}\n")

    if not attention or not settings["email_attention_events"]:
        return "Event logged. No attention email required."

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
        to_email=settings["attention_email"],
        subject=subject,
        body=body,
    )
