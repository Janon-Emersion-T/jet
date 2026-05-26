import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("storage/integrations")
BASE_DIR.mkdir(parents=True, exist_ok=True)

STATUS_FILE = BASE_DIR / "status.json"
DRAFTS_FILE = BASE_DIR / "drafts.json"
CONTACTS_FILE = BASE_DIR / "contacts.json"
CALENDAR_PROPOSALS_FILE = BASE_DIR / "calendar_proposals.json"


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def integration_status():
    status = _read_json(STATUS_FILE, {})
    defaults = {
        "gmail": {"connected": False, "mode": "draft-first", "last_checked": _now()},
        "calendar": {"connected": False, "mode": "proposal-first", "last_checked": _now()},
        "contacts": {"connected": False, "mode": "read-search-first", "last_checked": _now()},
        "whatsapp": {"connected": False, "mode": "draft-first", "last_checked": _now()},
    }
    defaults.update(status)
    _write_json(STATUS_FILE, defaults)
    return defaults


def save_gmail_draft(to, subject, body):
    drafts = _read_json(DRAFTS_FILE, [])
    draft = {
        "id": f"gmail_draft_{len(drafts)+1}",
        "type": "gmail",
        "to": to,
        "subject": subject,
        "body": body,
        "status": "draft_only",
        "created_at": _now(),
    }
    drafts.append(draft)
    _write_json(DRAFTS_FILE, drafts)
    return draft


def save_whatsapp_draft(to, message):
    drafts = _read_json(DRAFTS_FILE, [])
    draft = {
        "id": f"whatsapp_draft_{len(drafts)+1}",
        "type": "whatsapp",
        "to": to,
        "message": message,
        "status": "draft_only",
        "created_at": _now(),
    }
    drafts.append(draft)
    _write_json(DRAFTS_FILE, drafts)
    return draft


def propose_calendar_event(title, date, time, duration_minutes=60, notes=""):
    proposals = _read_json(CALENDAR_PROPOSALS_FILE, [])
    proposal = {
        "id": f"calendar_proposal_{len(proposals)+1}",
        "title": title,
        "date": date,
        "time": time,
        "duration_minutes": duration_minutes,
        "notes": notes,
        "status": "proposal_only",
        "created_at": _now(),
    }
    proposals.append(proposal)
    _write_json(CALENDAR_PROPOSALS_FILE, proposals)
    return proposal


def add_contact(name, email="", phone="", company=""):
    contacts = _read_json(CONTACTS_FILE, [])
    contact = {
        "id": f"contact_{len(contacts)+1}",
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "created_at": _now(),
    }
    contacts.append(contact)
    _write_json(CONTACTS_FILE, contacts)
    return contact


def search_contacts(query):
    contacts = _read_json(CONTACTS_FILE, [])
    q = query.lower()
    return [
        c for c in contacts
        if q in c.get("name", "").lower()
        or q in c.get("email", "").lower()
        or q in c.get("phone", "").lower()
        or q in c.get("company", "").lower()
    ]


def list_integration_drafts():
    return _read_json(DRAFTS_FILE, [])
