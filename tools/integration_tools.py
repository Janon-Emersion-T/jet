from __future__ import annotations

from tools.integration_status_tools import (
    add_contact,
    integration_status,
    list_integration_drafts as _list_integration_drafts,
    propose_calendar_event,
    save_gmail_draft,
    save_whatsapp_draft,
    search_contacts as _search_contacts,
)


def _format_bool(value: bool) -> str:
    return "connected" if value else "not connected"


def calendar_integration_help() -> str:
    status = integration_status().get("calendar", {})
    return "\n".join(
        [
            "CALENDAR INTEGRATION - PHASE 182",
            f"Status: {_format_bool(bool(status.get('connected', False)))}",
            f"Mode: {status.get('mode', 'proposal-first')}",
            "Safety: calendar changes are proposal-only until a human confirms them.",
        ]
    )


def gmail_integration_help() -> str:
    status = integration_status().get("gmail", {})
    return "\n".join(
        [
            "GMAIL INTEGRATION - PHASE 183",
            f"Status: {_format_bool(bool(status.get('connected', False)))}",
            f"Mode: {status.get('mode', 'draft-first')}",
            "Safety: Gmail actions should create drafts only unless sending is explicitly confirmed.",
        ]
    )


def contact_integration_help() -> str:
    status = integration_status().get("contacts", {})
    return "\n".join(
        [
            "CONTACT INTEGRATION - PHASE 184",
            f"Status: {_format_bool(bool(status.get('connected', False)))}",
            f"Mode: {status.get('mode', 'read-search-first')}",
            "Safety: contact workflows should search/read before creating outreach drafts.",
        ]
    )


def create_calendar_proposal(title: str, date: str, time: str, duration_minutes: int = 60, notes: str = "") -> str:
    proposal = propose_calendar_event(title, date, time, duration_minutes, notes)
    return "\n".join(
        [
            "CALENDAR PROPOSAL CREATED - PHASE 182",
            f"ID: {proposal['id']}",
            f"Title: {proposal['title']}",
            f"When: {proposal['date']} {proposal['time']}",
            f"Duration minutes: {proposal['duration_minutes']}",
            "Safety: this is a local proposal, not a live calendar write.",
        ]
    )


def gmail_draft_assistant(to_email: str, subject: str, body: str) -> str:
    draft = save_gmail_draft(to_email, subject, body)
    return "\n".join(
        [
            "GMAIL DRAFT ASSISTANT - PHASE 183",
            f"ID: {draft['id']}",
            f"To: {draft['to']}",
            f"Subject: {draft['subject']}",
            "Safety: this is a local draft. JARVIS will not send email automatically.",
        ]
    )


def add_local_contact(name: str, email: str = "", phone: str = "", company: str = "") -> str:
    contact = add_contact(name, email, phone, company)
    return f"LOCAL CONTACT SAVED - PHASE 184\nID: {contact['id']}\nName: {contact['name']}"


def search_contacts(query: str) -> str:
    matches = _search_contacts(query)
    if not matches:
        return "No matching contacts found."

    lines = ["CONTACT SEARCH RESULTS - PHASE 184"]
    for item in matches[:50]:
        lines.append(f"- {item['id']} | {item['name']} | {item.get('email') or '-'} | {item.get('phone') or '-'}")
    return "\n".join(lines)


def whatsapp_draft_assistant(request: str) -> str:
    request = request.strip() or "general client follow-up"
    message = (
        "Hello, this is Janon from LKProfessionals (Pvt) Ltd.\n\n"
        f"I wanted to follow up regarding {request}. Please let me know a convenient time to discuss the next steps.\n\n"
        "Thank you."
    )
    draft = save_whatsapp_draft("unspecified", message)
    return "\n".join(
        [
            "WHATSAPP DRAFT ASSISTANT - PHASE 185",
            f"ID: {draft['id']}",
            f"Request: {request}",
            "",
            "Draft:",
            message,
            "",
            "Safety: this is a local draft. JARVIS will not send WhatsApp messages automatically.",
        ]
    )


def list_integration_drafts() -> str:
    drafts = _list_integration_drafts()
    if not drafts:
        return "No integration drafts found."

    lines = ["INTEGRATION DRAFTS"]
    for item in reversed(drafts[-50:]):
        label = item.get("subject") or item.get("message") or item.get("to") or "draft"
        lines.append(f"- {item['id']} | {item['type']} | {item['status']} | {label}")
    return "\n".join(lines)


def integration_help() -> str:
    return """INTEGRATION COMMANDS - PHASES 182-185

182. calendar integration status
     calendar propose event <title> | <date> | <time>

183. gmail integration status
     gmail draft to <email> | <subject> | <message>

184. contact integration status
     add local contact <name> | <email optional> | <phone optional>
     search contacts <query>

185. whatsapp draft for <request>
"""
