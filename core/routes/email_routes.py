import re

from tools.email_tools import email_status, send_test_email, send_simple_email


EMAIL_PATTERN = r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"


def handle_email_routes(user_input: str, text: str, clean_text: str):
    raw = user_input.strip()

    if text in ["email status", "smtp status"]:
        return email_status()

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