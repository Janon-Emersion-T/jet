import re

from tools.email_tools import email_status, send_test_email, send_simple_email
from tools.event_tools import emit_event
from tools.notification_config import notification_status, save_notification_settings


EMAIL_PATTERN = r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"


def handle_email_routes(user_input: str, text: str, clean_text: str):
    raw = user_input.strip()

    if text in ["email status", "smtp status"]:
        return email_status()

    if text in ["notification status", "attention notifications", "alert email status"]:
        return notification_status()

    match = re.match(rf"^set attention email\s+{EMAIL_PATTERN}$", raw, re.IGNORECASE)
    if match:
        email = match.group(1).strip()
        save_notification_settings({"attention_email": email, "email_attention_events": True})
        return f"Attention-event emails enabled for {email}."

    if text in ["enable attention emails", "enable alert emails"]:
        save_notification_settings({"email_attention_events": True})
        return "Attention-event emails enabled."

    if text in ["disable attention emails", "disable alert emails"]:
        save_notification_settings({"email_attention_events": False})
        return "Attention-event emails disabled."

    if text in ["send attention test", "test attention email"]:
        return emit_event(
            "ATTENTION_TEST",
            "Attention notification test",
            "This test confirms that JARVIS attention notifications are configured.",
            requires_attention=True,
        )

    match = re.match(
        rf"^send test email to\s+{EMAIL_PATTERN}$",
        raw,
        re.IGNORECASE,
    )

    if match:
        return send_test_email(match.group(1).strip())

    match = re.match(
        rf"^send\s+(.+?)\s+email\s+to\s+{EMAIL_PATTERN}$",
        raw,
        re.IGNORECASE,
    )

    if match:
        message = match.group(1).strip()
        to_email = match.group(2).strip()
        return send_simple_email(to_email, message)

    match = re.match(
        rf"^send this\s+(.+?)\s+to\s+{EMAIL_PATTERN}$",
        raw,
        re.IGNORECASE,
    )

    if match:
        message = match.group(1).strip(" ,.")
        to_email = match.group(2).strip()
        return send_simple_email(to_email, message)

    match = re.match(
        rf"^(.+?),?\s*send this to\s+{EMAIL_PATTERN}$",
        raw,
        re.IGNORECASE,
    )

    if match:
        message = match.group(1).strip(" ,.")
        to_email = match.group(2).strip()
        return send_simple_email(to_email, message)

    match = re.match(
        rf"^send this\s+(.+?),?\s*send this to\s+{EMAIL_PATTERN}$",
        raw,
        re.IGNORECASE,
    )

    if match:
        message = match.group(1).strip(" ,.")
        to_email = match.group(2).strip()
        return send_simple_email(to_email, message)

    return None
