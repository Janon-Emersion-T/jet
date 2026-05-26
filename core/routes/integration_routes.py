from tools.integration_status_tools import (
    integration_status,
    save_gmail_draft,
    save_whatsapp_draft,
    propose_calendar_event,
    add_contact,
    search_contacts,
    list_integration_drafts,
)


def handle_integration_routes(user_input: str, text: str = None, clean_text: str = None):
    cmd = user_input.strip()

    if cmd == "integration help":
        return (
            "INTEGRATION COMMANDS\n"
            "- integration status\n"
            "- integration drafts\n"
            "- gmail draft email to <email> subject <subject> body <body>\n"
            "- calendar propose event title <title> date <YYYY-MM-DD> time <HH:MM> duration <minutes>\n"
            "- contact add <name> email <email> phone <phone> company <company>\n"
            "- contact search <query>\n"
            "- whatsapp draft to <name/number> message <message>\n\n"
            "Safety: Gmail, Calendar, Contacts, and WhatsApp are draft/proposal/read-first only."
        )

    if cmd == "integration status":
        return integration_status()

    if cmd == "integration drafts":
        return list_integration_drafts()

    if cmd.startswith("gmail draft email to ") and " subject " in cmd and " body " in cmd:
        raw = cmd.replace("gmail draft email to ", "", 1)
        to, rest = raw.split(" subject ", 1)
        subject, body = rest.split(" body ", 1)
        return save_gmail_draft(to.strip(), subject.strip(), body.strip())

    if cmd.startswith("whatsapp draft to ") and " message " in cmd:
        raw = cmd.replace("whatsapp draft to ", "", 1)
        to, message = raw.split(" message ", 1)
        return save_whatsapp_draft(to.strip(), message.strip())

    if cmd.startswith("calendar propose event title ") and " date " in cmd and " time " in cmd:
        raw = cmd.replace("calendar propose event title ", "", 1)
        title, rest = raw.split(" date ", 1)
        date, rest = rest.split(" time ", 1)

        duration = 60
        notes = ""

        if " duration " in rest:
            time_part, duration_part = rest.split(" duration ", 1)
            try:
                duration = int(duration_part.strip().split()[0])
            except Exception:
                duration = 60
        else:
            time_part = rest

        return propose_calendar_event(title.strip(), date.strip(), time_part.strip(), duration, notes)

    if cmd.startswith("contact add "):
        raw = cmd.replace("contact add ", "", 1)

        name = raw
        email = ""
        phone = ""
        company = ""

        if " email " in raw:
            name, rest = raw.split(" email ", 1)
            if " phone " in rest:
                email, rest = rest.split(" phone ", 1)
                if " company " in rest:
                    phone, company = rest.split(" company ", 1)
                else:
                    phone = rest
            elif " company " in rest:
                email, company = rest.split(" company ", 1)
            else:
                email = rest

        return add_contact(name.strip(), email.strip(), phone.strip(), company.strip())

    if cmd.startswith("contact search "):
        query = cmd.replace("contact search ", "", 1).strip()
        return search_contacts(query)

    return None
