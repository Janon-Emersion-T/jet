from pathlib import Path
from datetime import datetime
import json

INTEGRATION_DIR = Path("storage/integrations")
LOG_FILE = INTEGRATION_DIR / "integration_notes.json"


def _ensure():
    INTEGRATION_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.write_text(json.dumps([], indent=4), encoding="utf-8")


def _load():
    _ensure()
    try:
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(items):
    _ensure()
    LOG_FILE.write_text(json.dumps(items, indent=4), encoding="utf-8")


def _record(kind: str, content: str):
    items = _load()
    item = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "kind": kind,
        "content": content,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    items.append(item)
    _save(items)
    return item


def calendar_integration_help() -> str:
    return """CALENDAR INTEGRATION — PHASE 182

Current Mode:
Local planning stub only. No external calendar is connected yet.

Recommended Future Safe Flow:
1. Connect Google Calendar API.
2. Read events first.
3. Draft event changes.
4. Require confirmation before creating/updating/deleting events.

Command:
calendar integration status
"""


def gmail_integration_help() -> str:
    return """GMAIL INTEGRATION — PHASE 183

Current Mode:
Draft-only safety stub. JARVIS must not send emails automatically.

Recommended Future Safe Flow:
1. Read inbox only after permission.
2. Draft replies locally.
3. Confirm before creating Gmail draft.
4. Confirm again before sending.

Command:
gmail integration status
"""


def contact_integration_help() -> str:
    return """CONTACT INTEGRATION — PHASE 184

Current Mode:
Local contact planning stub only.

Recommended Future Safe Flow:
1. Read-only contact search first.
2. No automatic mass messaging.
3. Require confirmation before outreach actions.

Command:
contact integration status
"""


def whatsapp_draft_assistant(request: str) -> str:
    request = request.strip() or "general client follow-up"
    _record("whatsapp_draft", request)

    return f"""WHATSAPP DRAFT ASSISTANT — PHASE 185

Request:
{request}

Draft:
Hello, this is Janon from LKProfessionals (Pvt) Ltd.

I wanted to follow up regarding {request}. Please let me know a convenient time to discuss the next steps.

Thank you.

Safety:
This is only a draft. JARVIS will not send WhatsApp messages automatically.
"""


def integration_help() -> str:
    return """INTEGRATION COMMANDS — PHASES 182–185

182. calendar integration status
183. gmail integration status
184. contact integration status
185. whatsapp draft for <request>
"""
