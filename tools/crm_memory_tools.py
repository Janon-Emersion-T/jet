import json
from pathlib import Path
from datetime import datetime

CRM_DIR = Path("storage/crm")
CLIENTS_FILE = CRM_DIR / "clients.json"
LEADS_FILE = CRM_DIR / "leads.json"
FOLLOWUPS_FILE = CRM_DIR / "followups.json"
INVOICE_REMINDERS_FILE = CRM_DIR / "invoice_reminders.json"
MEETING_NOTES_FILE = CRM_DIR / "meeting_notes.json"


def _ensure_file(path: Path, default):
    CRM_DIR.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default, indent=4), encoding="utf-8")


def _load(path: Path, default):
    _ensure_file(path, default)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save(path: Path, data):
    _ensure_file(path, [] if isinstance(data, list) else {})
    path.write_text(json.dumps(data, indent=4), encoding="utf-8")


def _id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def add_client_profile(name: str, details: str) -> str:
    clients = _load(CLIENTS_FILE, {})
    key = name.lower().strip()

    if not key:
        return "Client name is required."

    clients[key] = {
        "name": name.strip(),
        "details": details.strip(),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    _save(CLIENTS_FILE, clients)
    return f"Client profile saved: {name.strip()}"


def show_client_profile(name: str) -> str:
    clients = _load(CLIENTS_FILE, {})
    key = name.lower().strip()

    client = clients.get(key)
    if not client:
        return "Client profile not found."

    return f"""CLIENT PROFILE

Name: {client['name']}
Details:
{client['details']}

Updated: {client.get('updated_at')}
"""


def add_lead(name: str, details: str) -> str:
    leads = _load(LEADS_FILE, [])
    lead_id = _id()

    leads.append({
        "id": lead_id,
        "name": name.strip(),
        "details": details.strip(),
        "status": "new",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    })

    _save(LEADS_FILE, leads)
    return f"Lead added: {lead_id} | {name.strip()}"


def list_leads() -> str:
    leads = _load(LEADS_FILE, [])

    if not leads:
        return "No leads found."

    lines = ["LEAD TRACKING"]
    for lead in reversed(leads[-50:]):
        lines.append(f"- {lead['id']} | {lead['status']} | {lead['name']} | {lead['details']}")

    return "\n".join(lines)


def set_lead_status(lead_id: str, status: str) -> str:
    leads = _load(LEADS_FILE, [])
    found = False

    for lead in leads:
        if lead["id"] == lead_id:
            lead["status"] = status
            lead["updated_at"] = datetime.now().isoformat(timespec="seconds")
            found = True
            break

    if not found:
        return "Lead not found."

    _save(LEADS_FILE, leads)
    return f"Lead {lead_id} updated to: {status}"


def add_follow_up(name: str, note: str) -> str:
    followups = _load(FOLLOWUPS_FILE, [])
    followup_id = _id()

    followups.append({
        "id": followup_id,
        "name": name.strip(),
        "note": note.strip(),
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })

    _save(FOLLOWUPS_FILE, followups)
    return f"Follow-up added: {followup_id} | {name.strip()}"


def list_follow_ups() -> str:
    followups = _load(FOLLOWUPS_FILE, [])

    if not followups:
        return "No follow-ups found."

    lines = ["FOLLOW-UP REMINDERS"]
    for item in reversed(followups[-50:]):
        lines.append(f"- {item['id']} | {item['status']} | {item['name']} | {item['note']}")

    return "\n".join(lines)


def invoice_reminder(client: str, details: str) -> str:
    reminders = _load(INVOICE_REMINDERS_FILE, [])
    reminder_id = _id()

    reminders.append({
        "id": reminder_id,
        "client": client.strip(),
        "details": details.strip(),
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })

    _save(INVOICE_REMINDERS_FILE, reminders)
    return f"Invoice reminder saved: {reminder_id} | {client.strip()}"


def list_invoice_reminders() -> str:
    reminders = _load(INVOICE_REMINDERS_FILE, [])

    if not reminders:
        return "No invoice reminders found."

    lines = ["INVOICE REMINDERS"]
    for item in reversed(reminders[-50:]):
        lines.append(f"- {item['id']} | {item['status']} | {item['client']} | {item['details']}")

    return "\n".join(lines)


def summarize_meeting(notes: str) -> str:
    notes = notes.strip()
    if not notes:
        return "Meeting notes are required."

    summary_id = _id()

    summary = {
        "id": summary_id,
        "raw_notes": notes,
        "summary": _basic_summary(notes),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    items = _load(MEETING_NOTES_FILE, [])
    items.append(summary)
    _save(MEETING_NOTES_FILE, items)

    return f"""MEETING NOTE SUMMARY

ID: {summary_id}

Summary:
{summary['summary']}

Saved to local CRM memory.
"""


def _basic_summary(notes: str) -> str:
    lines = [line.strip() for line in notes.replace(".", ".\n").splitlines() if line.strip()]
    key_lines = lines[:8]

    return "\n".join(f"- {line}" for line in key_lines)


def crm_help() -> str:
    return """CRM MEMORY COMMANDS — PHASES 177–181

177. add client profile <name> ::: <details>
     show client profile <name>

178. add lead <name> ::: <details>
     list leads
     set lead <lead_id> <status>

179. add follow up <name> ::: <note>
     list follow ups

180. invoice reminder for <client> ::: <details>
     list invoice reminders

181. summarize meeting ::: <notes>
"""
