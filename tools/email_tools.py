import os
import smtplib
from email.message import EmailMessage

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - fallback for partial installs
    def load_dotenv(*_args, **_kwargs):
        return False

load_dotenv()


def _smtp_config():
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "email": os.getenv("SMTP_EMAIL"),
        "password": os.getenv("SMTP_PASSWORD"),
        "from_name": os.getenv("SMTP_FROM_NAME", "JARVIS"),
        "dry_run": os.getenv("EMAIL_DRY_RUN", "true").lower() == "true",
    }


def email_status():
    config = _smtp_config()

    if not config["email"] or not config["password"]:
        return """EMAIL STATUS

SMTP is not configured.

Required .env values:
SMTP_EMAIL
SMTP_PASSWORD"""

    return f"""EMAIL STATUS

SMTP configured: YES
Email: {config["email"]}
Host: {config["host"]}
Port: {config["port"]}
Dry run: {"ON" if config["dry_run"] else "OFF"}

Safety:
Dry run should stay ON until test email is verified."""


def send_test_email(to_email: str):
    config = _smtp_config()

    if not config["email"] or not config["password"]:
        return "SMTP is not configured. Check your .env file."

    subject = "JARVIS Email Test"
    body = "This is a test email from JARVIS. SMTP configuration is working."

    if config["dry_run"]:
        return f"""EMAIL DRY RUN

To: {to_email}
Subject: {subject}

{body}

No email was sent because EMAIL_DRY_RUN=true."""

    msg = EmailMessage()
    msg["From"] = f'{config["from_name"]} <{config["email"]}>'
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(config["host"], config["port"]) as server:
            server.starttls()
            server.login(config["email"], config["password"])
            server.send_message(msg)

        return f"Test email sent successfully to {to_email}."

    except Exception as e:
        return f"Email sending failed: {e}"


def send_simple_email(to_email: str, message: str):
    config = _smtp_config()

    if not config["email"] or not config["password"]:
        return "SMTP is not configured. Check your .env file."

    subject = "Message from JARVIS"
    body = message.strip()

    if not body:
        return "Email message cannot be empty."

    if config["dry_run"]:
        return f"""EMAIL DRY RUN

To: {to_email}
Subject: {subject}

{body}

No email was sent because EMAIL_DRY_RUN=true."""

    msg = EmailMessage()
    msg["From"] = f'{config["from_name"]} <{config["email"]}>'
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(config["host"], config["port"]) as server:
            server.starttls()
            server.login(config["email"], config["password"])
            server.send_message(msg)

        return f"Email sent successfully to {to_email}."

    except Exception as e:
        return f"Email sending failed: {e}"
    
def send_system_email(to_email: str, subject: str, body: str):
    config = _smtp_config()

    if not config["email"] or not config["password"]:
        return "SMTP is not configured."

    msg = EmailMessage()
    msg["From"] = f'{config["from_name"]} <{config["email"]}>'
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(config["host"], config["port"]) as server:
            server.starttls()
            server.login(config["email"], config["password"])
            server.send_message(msg)

        return "System email sent."

    except Exception as e:
        return f"System email failed: {e}"
