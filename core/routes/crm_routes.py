from tools.crm_memory_tools import (
    add_client_profile,
    show_client_profile,
    add_lead,
    list_leads,
    set_lead_status,
    add_follow_up,
    list_follow_ups,
    invoice_reminder,
    list_invoice_reminders,
    summarize_meeting,
    crm_help,
)


def handle_crm_routes(user_input: str, text: str, clean_text: str):
    if text in ["crm help", "client memory help", "lead tracking help"]:
        return crm_help()

    if text.startswith("add client profile "):
        command = user_input.replace("add client profile ", "", 1).strip()
        if ":::" not in command:
            return "Invalid format. Use: add client profile <name> ::: <details>"
        name, details = command.split(":::", 1)
        return add_client_profile(name.strip(), details.strip())

    if text.startswith("show client profile "):
        name = user_input.replace("show client profile ", "", 1).strip()
        return show_client_profile(name)

    if text.startswith("add lead "):
        command = user_input.replace("add lead ", "", 1).strip()
        if ":::" not in command:
            return "Invalid format. Use: add lead <name> ::: <details>"
        name, details = command.split(":::", 1)
        return add_lead(name.strip(), details.strip())

    if text in ["list leads", "show leads", "lead tracking"]:
        return list_leads()

    if text.startswith("set lead "):
        command = user_input.replace("set lead ", "", 1).strip()
        parts = command.split()

        if len(parts) < 2:
            return "Invalid format. Use: set lead <lead_id> <status>"

        return set_lead_status(parts[0], parts[1])

    if text.startswith("add follow up "):
        command = user_input.replace("add follow up ", "", 1).strip()
        if ":::" not in command:
            return "Invalid format. Use: add follow up <name> ::: <note>"
        name, note = command.split(":::", 1)
        return add_follow_up(name.strip(), note.strip())

    if text in ["list follow ups", "show follow ups", "follow up reminders"]:
        return list_follow_ups()

    if text.startswith("invoice reminder for "):
        command = user_input.replace("invoice reminder for ", "", 1).strip()
        if ":::" not in command:
            return "Invalid format. Use: invoice reminder for <client> ::: <details>"
        client, details = command.split(":::", 1)
        return invoice_reminder(client.strip(), details.strip())

    if text in ["list invoice reminders", "show invoice reminders"]:
        return list_invoice_reminders()

    if text.startswith("summarize meeting :::"):
        notes = user_input.split(":::", 1)[1].strip()
        return summarize_meeting(notes)

    return None
