from pathlib import Path
        lines.append(f"- {item['id']} | {item['name']} | {item.get('email') or '-'} | {item.get('phone') or '-'}")
    return "\n".join(lines)


def list_local_contacts() -> str:
    contacts = _read_json(CONTACT_FILE, [])
    if not contacts:
        return "No local contacts found."

    lines = ["LOCAL CONTACTS"]
    for item in reversed(contacts[-50:]):
        lines.append(f"- {item['id']} | {item['name']} | {item.get('email') or '-'} | {item.get('phone') or '-'}")
    return "\n".join(lines)


def whatsapp_draft_assistant(request: str) -> str:
    request = request.strip() or "general client follow-up"

    draft_text = (
        "Hello, this is Janon from LKProfessionals (Pvt) Ltd.\n\n"
        f"I wanted to follow up regarding {request}. Please let me know a convenient time to discuss the next steps.\n\n"
        "Thank you."
    )

    draft = _save_draft("whatsapp", {
        "request": request,
        "message": draft_text,
    })

    return f"""WHATSAPP DRAFT ASSISTANT — PHASE 185

ID: {draft['id']}
Request:
{request}

Draft:
{draft_text}

Safety:
This is only a local draft. JARVIS will not send WhatsApp messages automatically.
"""


def list_integration_drafts() -> str:
    drafts = _read_json(DRAFT_FILE, [])
    if not drafts:
        return "No integration drafts found."

    lines = ["INTEGRATION DRAFTS"]
    for item in reversed(drafts[-50:]):
        payload = item.get("payload", {})
        label = payload.get("subject") or payload.get("request") or payload.get("to") or "draft"
        lines.append(f"- {item['id']} | {item['kind']} | {item['status']} | {label}")
    return "\n".join(lines)


def integration_help() -> str:
    return """INTEGRATION COMMANDS — PHASES 182–185

182. calendar integration status
     calendar propose event <title> | <start> | <end> | <location optional> | <notes optional>
     list calendar proposals

183. gmail integration status
     gmail draft to <email> | <subject> | <message>
     list integration drafts

184. contact integration status
     add local contact <name> | <email optional> | <phone optional> | <notes optional>
     search contacts <query>
     list local contacts

185. whatsapp draft for <request>

Config:
integration config status
"""